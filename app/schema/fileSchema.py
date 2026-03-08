from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    filename: str
    path: str