
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.services.llm_service import LLMService
from app.services.file_service import FileService
from app.models.quiz_models import QuizResponse, Quiz
import json

router = APIRouter()
llm_service = LLMService()
file_service = FileService()

@router.post("/generate", response_model=QuizResponse)
async def generate_quizzes(
    file: UploadFile = File(...),
    note_id: str = Form(...),
    exists_quizzes: str = Form(...)
):
    try:
        # 파일 형식 검증
        if not file_service.validate_file_type(file):
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

        # 텍스트 추출
        try:
            text = file_service.extract_text(file)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # 기존 퀴즈 파싱
        try:
            existing_quizzes = [Quiz.model_validate(quiz) for quiz in json.loads(exists_quizzes)]
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="잘못된 퀴즈 데이터 형식입니다.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"퀴즈 데이터 파싱 오류: {str(e)}")
        
        # 노트 및 퀴즈 생성
        try:
            notes, quizzes = await llm_service.process_document(text, existing_quizzes)
            # 결과를 출력하거나 로그에 기록
            print("노트 생성 완료")
            print(f"노트 내용: {notes[:100]}...")
            print(f"생성된 퀴즈 수: {len(quizzes)}")
            return QuizResponse(notes=notes, quizzes=quizzes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"퀴즈 생성 오류: {str(e)}")
            
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
