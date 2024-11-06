import time
from fastapi import UploadFile
import PyPDF2
import docx
import markdown
import io

class FileService:
    @staticmethod
    def extract_text(file: UploadFile) -> str:
        """다양한 형식의 파일에서 텍스트를 추출하는 메서드"""
        try:
            # 걸리는 시간 측정
            start_time = time.time()

            file_content = io.BytesIO(file.file.read())
            
            if file_content.getbuffer().nbytes == 0:
                raise ValueError("파일이 비어있습니다.")
                
            if file.content_type == "application/pdf":
                # PDF 처리
                pdf_reader = PyPDF2.PdfReader(file_content)
                text = "\n".join([page.extract_text() for page in pdf_reader.pages])
            
            elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # Word 문서 처리
                doc = docx.Document(file_content)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            elif file.content_type == "text/markdown":
                # Markdown 처리
                content = file_content.read().decode('utf-8')
                html = markdown.markdown(content)
                text = html.replace('<p>', '').replace('</p>', '\n')
            
            elif file.content_type == "text/plain":
                # 일반 텍스트 처리
                text = file_content.read().decode('utf-8')
            
            else:
                raise ValueError("지원하지 않는 파일 형식입니다.")
            
            if not text.strip():
                raise ValueError("추출된 텍스트가 비어있습니다.")
                
            end_time = time.time()
            print(f"텍스트 추출 완료: {end_time - start_time:.2f}초 소요")
            return text.strip()
            
        except Exception as e:
            raise ValueError(f"텍스트 추출 실패: {str(e)}")

    @staticmethod
    def validate_file_type(file: UploadFile) -> bool:
        """파일 형식 검증"""
        supported_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/markdown",
            "text/plain"
        ]
        return file.content_type in supported_types
