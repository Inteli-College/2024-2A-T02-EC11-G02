from fastapi import FastAPI
from routers import modelVersion, saveImage
from dotenv import load_dotenv
from firebase_admin import credentials
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

# Include the saveImage router
app.include_router(saveImage.router)

# Other routers
# app.include_router(S3Router.router)
app.include_router(modelVersion.router)
# app.include_router(pullArrayBytes.router)

if "__main__" == __name__:
    import uvicorn
    uvicorn.run(app, port=8000)