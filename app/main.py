from fastapi import FastAPI
from app.routes import quizzes
from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LLM Quiz Service")

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM Quiz Service"}
