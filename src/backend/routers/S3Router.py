from fastapi import APIRouter

router = APIRouter()

@router.get("/S3")
def S3Router():
    return {}