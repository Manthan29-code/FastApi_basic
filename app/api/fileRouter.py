from fastapi import APIRouter , UploadFile , File
from typing import List 
FileRouter = APIRouter()
from app.services.fileService import saveFile

@FileRouter.post("/file/upload")
async def upload_file(file: UploadFile = File(...)):

    result = await saveFile(file)

    return {
        "message": "File uploaded successfully",
        "data": result
    }



@FileRouter.post("/file/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):

    uploaded_files = []

    for file in files:
        result = await saveFile(file)
        uploaded_files.append(result)

    return {
        "message": "Files uploaded successfully",
        "data": uploaded_files
    }