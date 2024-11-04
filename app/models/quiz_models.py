from pydantic import BaseModel
from typing import List

class Quiz(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class QuizResponse(BaseModel):
    notes: str
    quizzes: List[Quiz]
