from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
import json
import os

# 환경 변수 로드
load_dotenv()

client = TestClient(app)

def test_generate_quizzes():
    # API 키 확인
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        masked_key = f"{api_key[:8]}...{api_key[-4:]}"
        print(f"\nAPI Key loaded: {masked_key}")
    else:
        print("\nWARNING: OPENAI_API_KEY not found in environment variables!")
    
    # 현재 작업 디렉토리와 .env 파일 위치 확인
    print(f"Current working directory: {os.getcwd()}")
    print(f".env file exists: {os.path.exists('.env')}")
    
    with open("tests/sample.pdf", "rb") as f:
        response = client.post(
            "/quizzes/generate",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    data = response.json()
    
    print("\n=== 생성된 노트 ===")
    print(data["notes"])
    print("\n=== 생성된 퀴즈 ===")
    print(json.dumps(data["quizzes"], indent=2, ensure_ascii=False))
    
    assert "notes" in data
    assert "quizzes" in data
    assert isinstance(data["quizzes"], list)
