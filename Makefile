# Makefile

.PHONY: install dev start test docker-build docker-run

# 의존성 설치
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# 개발 모드로 서버 실행 (자동 재시작)
dev:
	@echo "Starting FastAPI server in development mode..."
	python run.py dev

# 프로덕션 모드로 서버 실행
start:
	@echo "Starting FastAPI server in production mode..."
	python run.py start

# 테스트 실행
test:
	@echo "Running tests..."
	pytest -s

pdf-test:
	@echo "Running tests..."
	python3 test_run.py pdf sample.pdf

# Docker 이미지 빌드
docker-build:
	@echo "Building Docker image..."
	docker build -t llm-service .

# Docker 컨테이너 실행
docker-run:
	@echo "Running Docker container..."
	docker run -d --name llm-service -p 8000:8000 --env-file .env llm-service
