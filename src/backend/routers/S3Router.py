from fastapi import APIRouter

router = APIRouter()

@router.get("/S3")
def pull_array_bytes():
    return {}