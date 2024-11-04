# app/utils/text_extraction.py
import PyPDF2
import docx
from fastapi import UploadFile

def extract_text(file: UploadFile) -> str:
    try:
        if file.content_type == "application/pdf":
            reader = PyPDF2.PdfReader(file.file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text() is not None])
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file.file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif file.content_type == "text/plain":
            text = file.file.read().decode('utf-8')
        else:
            text = ""
    except Exception as e:
        text = ""
    return text
