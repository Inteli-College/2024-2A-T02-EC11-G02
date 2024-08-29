from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter()

@router.post("/uploadImage")
async def upload_image(file: UploadFile = File(...)):
    try:
        from ..main import bucket

        # Define the destination file name in Firebase Storage
        destination_blob_name = f"uploads/{file.filename}"

        # Get the blob (file) from the bucket
        blob = bucket.blob(destination_blob_name)

        # Upload the file content directly from the UploadFile object
        blob.upload_from_string(await file.read(), content_type=file.content_type)

        # Make the file publicly accessible (optional)
        blob.make_public()

        return {"message": "File uploaded successfully.", "file_url": blob.public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")