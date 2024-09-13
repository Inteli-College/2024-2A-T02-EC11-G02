from fastapi import APIRouter, UploadFile, File, HTTPException
from firebase_admin import storage
import zipfile
import io
import os

router = APIRouter()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Reference to the storage bucket
        bucket = storage.bucket()

        # Read the uploaded zip file in memory as bytes
        file_bytes = await file.read()
        
        # Create a BytesIO object from the file bytes
        file_like_object = io.BytesIO(file_bytes)
        
        # Try to unzip the file
        try:
            print("Unzipping file...")
            # Initialize a ZipFile object with the file-like object
            with zipfile.ZipFile(file_like_object) as zip_file:
                # Initialize a dictionary to hold file names and their byte contents
                extracted_files = {}

                print("Extracting files...")
                # Iterate over each file in the zip
                for file_name in zip_file.namelist():
                    # Open the file and read it as bytes
                    with zip_file.open(file_name) as extracted_file:
                        # Store the file name and its content as bytes in the dictionary
                        extracted_files[file_name] = extracted_file.read()
                
                # Upload each extracted file to Firebase Storage
                public_urls = []
                for file_name, file_content in extracted_files.items():
                    # Create a destination path for the uploaded file in Firebase
                    destination_blob_name = f"uploads/{file_name}"
                    blob = bucket.blob(destination_blob_name)

                    # Upload file to Firebase from the byte contents
                    blob.upload_from_string(file_content)

                    # Optional: Make the file public if public access is needed
                    blob.make_public()

                    # Store the public URL of the uploaded file
                    public_urls.append(blob.public_url)

                return {"message": "All files uploaded successfully!", "public_urls": public_urls}
        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail="Invalid ZIP file")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during extraction: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/unzip/")
async def unzip_file(file: UploadFile = File(...)):
    try:
        # Read the uploaded file in memory as bytes
        file_bytes = await file.read()
        
        # Create a BytesIO object from the file bytes
        file_like_object = io.BytesIO(file_bytes)
        
        # Initialize a ZipFile object with the file-like object
        with zipfile.ZipFile(file_like_object) as zip_file:
            # Initialize a dictionary to hold file names and their byte contents
            extracted_files = {}

            # Iterate over each file in the zip
            for file_name in zip_file.namelist():
                # Open the file and read it as bytes
                with zip_file.open(file_name) as extracted_file:
                    # Store the file name and its content as bytes in the dictionary
                    extracted_files[file_name] = extracted_file.read()

            # Return the extracted files and their byte contents
            return {"message": "Files extracted successfully!", "files": extracted_files}
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")