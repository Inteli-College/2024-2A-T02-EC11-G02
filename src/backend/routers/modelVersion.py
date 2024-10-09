from fastapi import APIRouter, File, UploadFile, HTTPException
from .tools.filtering_segmentation import FilteringSegmentation
from fastapi.responses import FileResponse
import shutil
import os
from tempfile import NamedTemporaryFile
from PIL import Image
import cv2
from pymongo import MongoClient
from firebase_admin import storage
import io
import zipfile

router = APIRouter()

client = MongoClient("mongodb://root:example@mongo:27017")
db = client["analise_ambiental"]
collection = db["resultados_modelo"]

@router.post("/modelversion")
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

        # Cria um novo arquivo temporário para salvar a imagem processada
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            Imagem = Image.fromarray(imagem)
            Imagem.save(tmp.name)
            
            tmp_path = tmp.name
        
        return FileResponse(tmp_path, filename=os.path.basename(tmp_path))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/firebase_url")
async def model_version(file: UploadFile = File(...)):
    try:
        # Crie um arquivo temporário para armazenar a imagem enviada
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        #print("Objeto copiado")
        # Inicializa o pipeline de processamento e processa a imagem
        pipeline = FilteringSegmentation()
        imagem_processada = await pipeline.segment_image_async(tmp_path)

        # Exclua o arquivo temporário original após o processamento
        os.remove(tmp_path)

        # Crie um novo arquivo temporário para salvar a imagem processada
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            # Converte o resultado para uma imagem do PIL e salva no arquivo temporário
            imagem_pil = Image.fromarray(imagem_processada)
            imagem_pil.save(tmp.name)
            
            processed_tmp_path = tmp.name

        # Carregar a imagem processada no Firebase Storage
        bucket = storage.bucket()  # Certifique-se de que a configuração do Firebase está correta
        print(f'Nome: {os.path.basename(processed_tmp_path)}')
        processed_blob_name = f"processed/{os.path.basename(processed_tmp_path)}"
        processed_blob = bucket.blob(processed_blob_name)

        # Codifique a imagem processada como PNG e faça o upload
        with open(processed_tmp_path, "rb") as processed_file:
            processed_blob.upload_from_file(processed_file, content_type='image/png')

        # Torne a URL da imagem pública
        processed_blob.make_public()
        processed_image_url = processed_blob.public_url

        # Exclua o arquivo temporário da imagem processada
        os.remove(processed_tmp_path)


        
        # Retorne a URL pública da imagem processada
        return {"processed_image_url": processed_image_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/upload_and_process/")
async def upload_and_process(file: UploadFile = File(...)):
    pipeline = None

    # Dicionários para URLs dos arquivos
    original_urls = []
    processed_urls = []
    documentos = []
    try:
        # Referência ao bucket de storage
        bucket = storage.bucket()

        # Lê o arquivo .zip recebido em memória como bytes
        file_bytes = await file.read()

        # Cria um objeto BytesIO a partir dos bytes do arquivo
        file_like_object = io.BytesIO(file_bytes)

        try:
            print("Unzipping file...")
            # Inicializa um objeto ZipFile com o arquivo em memória
            with zipfile.ZipFile(file_like_object) as zip_file:
                # Inicializa um dicionário para armazenar os nomes dos arquivos e seus conteúdos
                extracted_files = {}

                print("Extracting files...")
                # Extrai os arquivos do .zip
                for file_name in zip_file.namelist():
                    with zip_file.open(file_name) as extracted_file:
                        extracted_files[file_name] = extracted_file.read()
                print(f"Extracted files: {list(extracted_files.keys())}")

                # Processa cada imagem extraída do arquivo ZIP
                for file_name, file_content in extracted_files.items():
                    if file_name.endswith('/'):
                        print(f"Skipping directory: {file_name}")
                        continue

                    print(f"Processing file: {file_name}")

                    # Cria um arquivo temporário para armazenar a imagem original
                    with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        tmp.write(file_content)
                        tmp_path = tmp.name

                    print(f"Temporary file created at: {tmp_path}")

                    # Faz o upload da imagem original para Firebase Storage
                    original_blob_name = f"original/{file_name}"
                    original_blob = bucket.blob(original_blob_name)
                    original_blob.upload_from_string(file_content, content_type='image/png')
                    original_blob.make_public()  # Torna a URL pública
                    original_urls.append(original_blob.public_url)

                    print(f"Original image uploaded: {original_blob.public_url}")

                    # Inicializa o pipeline de processamento e processa a imagem
                    try:
                        # Verifica se a imagem foi salva corretamente
                        try:
                            with Image.open(tmp_path) as img:
                                img.verify()  # Verifica se o arquivo é realmente uma imagem
                                print(f"Image {file_name} is valid and has been saved correctly.")
                        except Exception as e:
                            print(f"Invalid image file: {str(e)}")
                            raise HTTPException(status_code=400, detail=f"Arquivo de imagem inválido: {str(e)}")
    
                        print("Starting image processing...")
                        pipeline = FilteringSegmentation()
                        processed_image = await pipeline.segment_image_async(tmp_path)
                        print("Image processed successfully.")

                        # Converte a imagem processada para o formato PNG em memória
                        success, encoded_image = cv2.imencode('.png', processed_image)
                        if not success:
                            raise HTTPException(status_code=500, detail="Falha ao codificar a imagem processada.")

                        processed_image_bytes = encoded_image.tobytes()

                        # Faz o upload da imagem processada para Firebase Storage
                        processed_blob_name = f"processed/{file_name}"
                        processed_blob = bucket.blob(processed_blob_name)
                        processed_blob.upload_from_string(processed_image_bytes, content_type='image/png')
                        processed_blob.make_public()  # Torna a URL pública
                        processed_urls.append(processed_blob.public_url)

                        print(f"Processed image uploaded: {processed_blob.public_url}")

                        documento = {
                            "modelo": "V1",
                            "margem_de_erro": 25,  # Margem de erro em percentual
                            "img": {
                                "url_imagem_processada": processed_blob.public_url,
                                "url_imagem_original": original_blob.public_url,
                                "quantidade_de_arvores": pipeline.counted,
                                "metros_quadrados_vegetacao": 5000
                            }
                        }
                        documentos.append(documento)
                    except Exception as e:
                        print(f"Error during image processing: {str(e)}")
                        raise HTTPException(status_code=500, detail=f"Error during image processing: {str(e)}")

                    # Remove o arquivo temporário após o processamento
                    os.remove(tmp_path)
                    print(f"Temporary file removed: {tmp_path}")
            #print(documentos)
            # Insere os documentos no banco de dados
            for documento in documentos:
                collection.insert_one(documento)
            return {
                    "message": "Imagens processadas e enviadas com sucesso!",
                    "original_urls": original_urls,
                    "processed_urls": processed_urls
                }

        except zipfile.BadZipFile:
            print("Invalid ZIP file.")
            raise HTTPException(status_code=400, detail="Arquivo ZIP inválido")
        except Exception as e:
            print(f"Error during extraction: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro durante a extração: {str(e)}")

    except Exception as e:
        print(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro: {str(e)}")
