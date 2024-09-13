from fastapi import APIRouter, File, UploadFile, HTTPException
from .code.apply_filter import FilteringSegmentation
import shutil
import os
from tempfile import NamedTemporaryFile

router = APIRouter()

@router.post("/modelversion")
async def modelVersion(file: UploadFile = File(...)):
    try:
        # Create a temporary file to store the uploaded image
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Initialize the pipeline and pass the temporary file path to the method
        pipeline = FilteringSegmentation()
        imagem = pipeline.hailht_extractor(tmp_path)
        
        # Optionally, delete the temporary file after processing
        os.remove(tmp_path)
        
        return imagem

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
