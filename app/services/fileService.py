import os 
from fastapi import UploadFile
from uuid import uuid4

UPLOAD_DIR = "app/uploads"

async def saveFile( file : UploadFile ):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
    "filename": unique_filename,
    "path": file_path
    }

# import asyncio
# from pathlib import Path

# def _delete_files(folder_path: str):
#     folder = Path(folder_path)

#     if not folder.exists():
#         return

#     for file in folder.iterdir():
#         if file.is_file():
#             file.unlink()

# async def delete_all_files(folder_path: str):
#     await asyncio.to_thread(_delete_files, folder_path)