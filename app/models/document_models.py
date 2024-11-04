# app/models/document_models.py
from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    notes: str
    quizzes: list
