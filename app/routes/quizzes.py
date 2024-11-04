# app/routes/quizzes.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.llm_service import LLMService
from app.services.file_service import FileService
from app.models.quiz_models import QuizResponse

router = APIRouter()
llm_service = LLMService()
file_service = FileService()

@router.post("/generate", response_model=QuizResponse)
async def generate_quizzes(file: UploadFile = File(...)):
    # 파일 형식 검증
    if not file_service.validate_file_type(file):
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    # 텍스트 추출
    text = file_service.extract_text(file)
    if not text:
        raise HTTPException(status_code=400, detail="텍스트 추출에 실패했습니다.")

    # LLM을 사용하여 노트 및 퀴즈 생성
    notes, quizzes = llm_service.generate_notes_and_quizzes(text)
    
    return QuizResponse(notes=notes, quizzes=quizzes)
