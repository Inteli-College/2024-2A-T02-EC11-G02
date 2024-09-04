from fastapi import APIRouter

router = APIRouter()

@router.get("/modelversion")
def modelVersion():
    return {}