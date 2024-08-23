from fastapi import APIRouter

router = APIRouter()

@router.get("/modelversion")
def model_version():
    return {}