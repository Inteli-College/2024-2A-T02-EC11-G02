from fastapi import APIRouter, File, UploadFile, HTTPException
from .tools.filtering_segmentation import FilteringSegmentation
from fastapi.responses import FileResponse
import shutil
import os
from tempfile import NamedTemporaryFile
import cv2
from PIL import Image
from pymongo import MongoClient
from firebase_admin import storage
import io
import zipfile
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading
import asyncio

router = APIRouter()

client = MongoClient("mongodb://root:example@mongo:27017")
db = client["analise_ambiental"]
collection = db["resultados_modelo"]

@router.post("/modelversion") # Testar
async def modelVersion(file: UploadFile = File(...)) :
    try:
        # Create a temporary file to store the uploaded image
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Initialize the pipeline and pass the temporary file path to the method
        pipeline = FilteringSegmentation()
        imagem = await pipeline.segment_image_async(tmp_path)

        # Opcionalmente, exclua o arquivo temporário após o processamento
        os.remove(tmp_path)
        imagem_processada_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
        # Cria um novo arquivo temporário para salvar a imagem processada
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            cv2.imwrite(tmp.name, imagem_processada_bgr)
            tmp_path = tmp.name
        
        return FileResponse(tmp_path, filename=os.path.basename(tmp_path))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def save_and_upload_image_to_firebase(image, suffix, folder="processed"):
    # Converte a imagem para BGR se necessário
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Crie um novo arquivo temporário para salvar a imagem processada
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        # Salva a imagem processada diretamente no arquivo temporário
        cv2.imwrite(tmp.name, image_bgr)
        tmp_path = tmp.name

    # Carregar a imagem no Firebase Storage
    bucket = storage.bucket()  # Certifique-se de que a configuração do Firebase está correta
    print(f'Nome: {os.path.basename(tmp_path)}')
    blob_name = f"{folder}/{os.path.basename(tmp_path)}"
    blob = bucket.blob(blob_name)

    # Codifique a imagem como PNG e faça o upload
    with open(tmp_path, "rb") as tmp_file:
        blob.upload_from_file(tmp_file, content_type='image/png')

    # Torne a URL da imagem pública
    blob.make_public()
    image_url = blob.public_url

    # Exclua o arquivo temporário
    os.remove(tmp_path)

    return image_url

from concurrent.futures import ThreadPoolExecutor
from fastapi import BackgroundTasks

# Função auxiliar para fazer o upload de uma imagem no Firebase
def upload_image_to_firebase(image, suffix=".png"):
    try:
        return save_and_upload_image_to_firebase(image, suffix)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")


@router.post("/firebase_url")
async def model_version(file: UploadFile = File(...)):
    try:
        # Verifique se o arquivo foi enviado
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        try:
            # Crie um arquivo temporário para armazenar a imagem enviada
            with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")

        try:
            # Inicializa o pipeline de processamento e processa a imagem
            pipeline = FilteringSegmentation()
            imagem_processada = await pipeline.segment_image_async(tmp_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")
        finally:
            # Exclua o arquivo temporário original após o processamento
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        try:
            # Executa o upload das imagens processada e colorida em threads separadas
            with ThreadPoolExecutor() as executor:
                future_processed = executor.submit(upload_image_to_firebase, imagem_processada, ".png")
                future_colorized = executor.submit(upload_image_to_firebase, pipeline.masked_image, ".png")

                # Aguarda que ambas as tarefas de upload sejam concluídas
                processed_image_url = future_processed.result()
                colorize_processed_image_url = future_colorized.result()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload images: {str(e)}")

        # Retorne as URLs públicas das imagens e outros dados do pipeline
        return {
            "processed_image_url": processed_image_url,
            "colorize_processed_image_url": colorize_processed_image_url,
            "version": pipeline.model_version,
            "counted": pipeline.counted,
        }

    except HTTPException as e:
        # Captura e lança exceções específicas
        raise e
    except Exception as e:
        # Captura qualquer outra exceção não tratada
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



# Função para verificar se o arquivo ZIP é válido e extrair os arquivos
async def extract_files_from_zip(file_bytes):
    try:
        # Cria um objeto BytesIO a partir dos bytes do arquivo
        file_like_object = io.BytesIO(file_bytes)
        extracted_files = {}

        # Inicializa um objeto ZipFile com o arquivo em memória
        with zipfile.ZipFile(file_like_object) as zip_file:
            print("Extracting files...")
            for file_name in zip_file.namelist():
                with zip_file.open(file_name) as extracted_file:
                    if file_name.endswith('/'):
                        print(f"Skipping directory: {file_name}")
                        continue
                    extracted_files[file_name] = extracted_file.read()
        print(f"Extracted files: {list(extracted_files.keys())}")
        return extracted_files
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Arquivo ZIP inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a extração: {str(e)}")

# Função para processar a imagem e verificar a validade
def verify_and_process_image(file_name, file_content):
    try:
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        # Verifica se o arquivo temporário é uma imagem válida
        try:
            with Image.open(tmp_path) as img:
                img.verify()  # Verifica se o arquivo é uma imagem válida
                print(f"Image {file_name} is valid.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Arquivo de imagem inválido: {str(e)}")

        return tmp_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar a imagem: {str(e)}")

# Função para processar a imagem com o pipeline
async def process_image_with_pipeline(tmp_path, file_name, bucket):
    try:
        # Inicializa o pipeline de processamento
        pipeline = FilteringSegmentation()
        processed_image = await pipeline.segment_image_async(tmp_path)

        # Converte a imagem processada para o formato PNG
        success, encoded_image = cv2.imencode('.png', processed_image)
        if not success:
            raise HTTPException(status_code=500, detail="Falha ao codificar a imagem processada.")
        processed_image_bytes = encoded_image.tobytes()

        # Faz o upload da imagem processada para o Firebase Storage
        processed_blob_name = f"processed/{file_name}"
        processed_blob = bucket.blob(processed_blob_name)
        processed_blob.upload_from_string(processed_image_bytes, content_type='image/png')
        processed_blob.make_public()

        print(f"Processed image uploaded: {processed_blob.public_url}")
        return processed_blob.public_url, pipeline.counted

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during image processing: {str(e)}")
    finally:
        # Remove o arquivo temporário após o processamento
        os.remove(tmp_path)
        print(f"Temporary file removed: {tmp_path}")

# Função para fazer o upload de uma imagem original para o Firebase Storage
def upload_original_image_to_firebase(file_name, file_content, bucket):
    try:
        original_blob_name = f"original/{file_name}"
        original_blob = bucket.blob(original_blob_name)
        original_blob.upload_from_string(file_content, content_type='image/png')
        original_blob.make_public()

        print(f"Original image uploaded: {original_blob.public_url}")
        return original_blob.public_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer o upload da imagem original: {str(e)}")



@router.post("/upload_and_process/")
async def upload_and_process(file: UploadFile = File(...)):
    try:
        # Referência ao bucket de storage
        bucket = storage.bucket()

        # Lê o arquivo .zip recebido em memória
        file_bytes = await file.read()

        # Extrai os arquivos do ZIP
        extracted_files = await extract_files_from_zip(file_bytes)

        # Dicionários para armazenar as URLs e documentos
        original_urls = []
        processed_urls = []
        documentos = []

        # Função para processar cada arquivo usando threads
        def process_file(file_name, file_content):
            try:
                print(f"Processing file: {file_name}")

                # Verifica e processa a imagem original
                tmp_path = verify_and_process_image(file_name, file_content)

                # Faz o upload da imagem original para o Firebase
                original_url = upload_original_image_to_firebase(file_name, file_content, bucket)
                original_urls.append(original_url)

                # Processa a imagem com o pipeline e faz o upload
                loop = asyncio.new_event_loop()  # Cria um novo event loop para rodar código assíncrono em threads
                asyncio.set_event_loop(loop)
                processed_url, counted_trees = loop.run_until_complete(process_image_with_pipeline(tmp_path, file_name, bucket))
                processed_urls.append(processed_url)

                # Cria o documento a ser armazenado
                documento = {
                    "modelo": "V1",
                    "margem_de_erro": 25,  # Margem de erro em percentual
                    "img": {
                        "url_imagem_processada": processed_url,
                        "url_imagem_original": original_url,
                        "quantidade_de_arvores": counted_trees,
                        "metros_quadrados_vegetacao": 5000
                    }
                }
                documentos.append(documento)
            except Exception as e:
                print(f"Error processing file {file_name}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Erro no processamento do arquivo {file_name}: {str(e)}")

        # Thread-safe lock para garantir que as listas sejam modificadas de forma segura
        lock = threading.Lock()

        # Executor para rodar threads
        with ThreadPoolExecutor() as executor:
            # Submete uma tarefa para cada arquivo extraído
            futures = [
                executor.submit(process_file, file_name, file_content)
                for file_name, file_content in extracted_files.items()
            ]

            # Espera todas as threads terminarem
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # Se alguma thread falhar, result() levantará a exceção
                except Exception as e:
                    print(f"Thread error: {str(e)}")
                    raise HTTPException(status_code=500, detail=f"Ocorreu um erro na thread: {str(e)}")

        # Insere os documentos no banco de dados após todas as threads concluírem
        collection.insert_many(documentos)

        return {
            "message": "Imagens processadas e enviadas com sucesso!",
            "original_urls": original_urls,
            "processed_urls": processed_urls
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro: {str(e)}")