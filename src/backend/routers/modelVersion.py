from fastapi import APIRouter, File, UploadFile, HTTPException
from .tools.filtering_segmentation import FilteringSegmentation
from fastapi.responses import FileResponse
import shutil
import os
from tempfile import NamedTemporaryFile
from PIL import Image

router = APIRouter()

@router.post("/modelversion")
async def modelVersion(file: UploadFile = File(...)) :
    try:
        # Create a temporary file to store the uploaded image
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Initialize the pipeline and pass the temporary file path to the method
        pipeline = FilteringSegmentation()
        imagem = await pipeline.segment_image_async(tmp_path)

        # Opcionalmente, exclua o arquivo temporário após o processamento
        os.remove(tmp_path)

        # Cria um novo arquivo temporário para salvar a imagem processada
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            Imagem = Image.fromarray(imagem)
            Imagem.save(tmp.name)
            
            tmp_path = tmp.name
        


        return FileResponse(tmp_path, filename=os.path.basename(tmp_path))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
