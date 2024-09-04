from fastapi import APIRouter

router = APIRouter()

@router.get("/array")
def pullArrayBytes():
    return {}