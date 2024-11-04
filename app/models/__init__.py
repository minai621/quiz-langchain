# app/models/__init__.py
from .quiz_models import Quiz, QuizResponse
from .document_models import DocumentUploadResponse

__all__ = ["Quiz", "QuizResponse", "DocumentUploadResponse"]
