from fastapi import FastAPI
from backend.routers import S3Router, modelVersion, saveImage, pullArrayBytes
from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import storage
import firebase_admin
import os

load_dotenv()

firebase_storage_bucket = os.getenv('FIREBASE_STORAGE_BUCKET')
firebase_key_path = os.getenv('FIREBASE_KEY_PATH')

current_directory = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_directory, firebase_key_path)
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_storage_bucket
})

bucket = storage.bucket()

# 'bucket' is an object defined in the google-cloud-storage Python library.
# See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
# for more details.

app = FastAPI()

app.include_router(S3Router.router)
app.include_router(saveImage.router)
app.include_router(modelVersion.router)
app.include_router(pullArrayBytes.router)

saveImage.upload_image(bucket)