from PIL import Image
import imagehash
from fastapi import APIRouter

router = APIRouter()

@router.get("/imagehash")
def model_version():
    image = Image.open('src/backend/routers/bode.webp')
    hash_value = imagehash.average_hash(image)
    return {hash_value}