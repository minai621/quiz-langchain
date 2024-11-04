from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
import io

class FileService:
    @staticmethod
    def extract_text(file: UploadFile) -> str:
        """파일에서 텍스트를 추출하는 메서드"""
        # 파일 내용을 메모리에 읽기
        file_content = io.BytesIO(file.file.read())
        
        if file.content_type == "application/pdf":
            # PDF 파일 처리
            pdf_reader = PdfReader(file_content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        else:
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")
    
    @staticmethod
    def validate_file_type(file: UploadFile) -> bool:
        """파일 형식이 지원되는지 확인하는 메서드"""
        supported_types = [
            "application/pdf"
        ]
        return file.content_type in supported_types
