from fastapi import APIRouter, File, UploadFile, HTTPException
from .code.apply_filter import FilteringSegmentation
import shutil
import os
from tempfile import NamedTemporaryFile
import zipfile
import io
from firebase_admin import storage


router = APIRouter()

@router.post("/modelversion")
async def modelVersion(file: UploadFile = File(...)):
    try:
        # Create a temporary file to store the uploaded image
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Initialize the pipeline and pass the temporary file path to the method
        pipeline = FilteringSegmentation()
        imagem = pipeline.hailht_extractor(tmp_path)
        
        # Optionally, delete the temporary file after processing
        os.remove(tmp_path)
        
        return imagem

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/upload_and_process/")
async def upload_and_process(file: UploadFile = File(...)):
    try:
        # Referência ao bucket de storage
        bucket = storage.bucket()

        # Lê o arquivo .zip recebido em memória como bytes
        file_bytes = await file.read()

        # Cria um objeto BytesIO a partir dos bytes do arquivo
        file_like_object = io.BytesIO(file_bytes)

        try:
            # Inicializa um objeto ZipFile com o arquivo em memória
            with zipfile.ZipFile(file_like_object) as zip_file:
                # Inicializa um dicionário para armazenar os nomes dos arquivos e seus conteúdos
                extracted_files = {}

                # Extrai os arquivos do .zip
                for file_name in zip_file.namelist():
                    with zip_file.open(file_name) as extracted_file:
                        extracted_files[file_name] = extracted_file.read()

                # Dicionários para URLs dos arquivos
                original_urls = []
                processed_urls = []

                # Processa cada imagem extraída do arquivo ZIP
                for file_name, file_content in extracted_files.items():
                    # Cria um arquivo temporário para armazenar a imagem original
                    with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        tmp.write(file_content)
                        tmp_path = tmp.name

                    # Faz o upload da imagem original para Firebase Storage
                    original_blob_name = f"original/{file_name}"
                    original_blob = bucket.blob(original_blob_name)
                    original_blob.upload_from_string(file_content)
                    original_blob.make_public()  # Torna a URL pública
                    original_urls.append(original_blob.public_url)

                    # Inicializa o pipeline de processamento e processa a imagem
                    pipeline = FilteringSegmentation()
                    processed_image = pipeline.hailht_extractor(tmp_path)

                    # Faz o upload da imagem processada para Firebase Storage
                    processed_blob_name = f"processada/{file_name}"
                    processed_blob = bucket.blob(processed_blob_name)
                    processed_blob.upload_from_string(processed_image)
                    processed_blob.make_public()  # Torna a URL pública
                    processed_urls.append(processed_blob.public_url)

                    # Remove o arquivo temporário após o processamento
                    os.remove(tmp_path)

                # Retorna as URLs públicas das imagens originais e processadas
                return {
                    "message": "Imagens processadas e enviadas com sucesso!",
                    "original_urls": original_urls,
                    "processed_urls": processed_urls
                }

        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail="Arquivo ZIP inválido")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro durante a extração: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro: {str(e)}")
