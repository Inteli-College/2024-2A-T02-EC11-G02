from fastapi import APIRouter

router = APIRouter()

@router.get("/array")
def pull_array_bytes():
    return {}