from fastapi import APIRouter, File, UploadFile, HTTPException
from .code.apply_filter import FilteringSegmentation
import shutil
import os
from tempfile import NamedTemporaryFile
import zipfile
import io
from firebase_admin import storage
from PIL import Image


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

                # Dicionários para URLs dos arquivos
                original_urls = []
                processed_urls = []

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
                    original_blob.upload_from_string(file_content)
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
                        processed_image = pipeline.hailht_extractor(tmp_path)
                        print("Image processed successfully.")

                        # # Verifique o tipo de processed_image
                        # if isinstance(processed_image, bytes):
                        #     processed_image_bytes = processed_image
                        # else:
                        #     processed_image_bytes = io.BytesIO()
                        #     processed_image.save(processed_image_bytes, format='PNG')
                        #     processed_image = processed_image_bytes.getvalue()

                        # Faz o upload da imagem processada para Firebase Storage
                        processed_blob_name = f"processada/{file_name}"
                        processed_blob = bucket.blob(processed_blob_name)
                        processed_blob.upload_from_string(processed_image)
                        processed_blob.make_public()  # Torna a URL pública
                        processed_urls.append(processed_blob.public_url)

                        print(f"Processed image uploaded: {processed_blob.public_url}")

                    except Exception as e:
                        print(f"Error during image processing: {str(e)}")
                        raise HTTPException(status_code=500, detail=f"Error during image processing: {str(e)}")

                    # Remove o arquivo temporário após o processamento
                    os.remove(tmp_path)
                    print(f"Temporary file removed: {tmp_path}")

                # Retorna as URLs públicas das imagens originais e processadas
                print("Processing completed successfully. Returning URLs.")
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
