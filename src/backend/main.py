from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
from backend.routers import S3Router, modelVersion, saveImage, pullArrayBytes

current_directory = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_directory, 'serviceAccountKey.json')
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'grupo2-93568-589050f73fa8.appspot.com'
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