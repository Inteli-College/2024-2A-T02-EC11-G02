from fastapi import FastAPI
from routers import modelVersion, saveImage, pullArrayBytes
from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import storage
import firebase_admin
import os

load_dotenv()
app = FastAPI()

firebase_storage_bucket = os.getenv('FIREBASE_STORAGE_BUCKET')
firebase_key_path = os.getenv('FIREBASE_KEY_PATH')

cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_storage_bucket
})

# Função para fazer upload da imagem para o Firebase Storage
def upload_image(file_path, destination_blob_name):
    # Referência ao bucket de armazenamento
    bucket = storage.bucket()
    
    # Referência ao local no storage onde a imagem será salva
    blob = bucket.blob(destination_blob_name)
    
    # Fazendo o upload da imagem
    blob.upload_from_filename(file_path)
    
    # Opcional: Tornar o arquivo público (caso precise de acesso público)
    blob.make_public()
    
    print(f"Imagem enviada com sucesso! URL pública: {blob.public_url}")

# Envie sua imagem
upload_image("bode.webp", "sucesso/bode.webp")

#app.include_router(S3Router.router)
#app.include_router(saveImage.router)
#app.include_router(modelVersion.router)
#app.include_router(pullArrayBytes.router)

#saveImage.upload_image("")

if "__main__" == __name__:
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)