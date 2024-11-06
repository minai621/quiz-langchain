from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum
from langchain_core.prompts import PromptTemplate

class QuizType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"  # 추가
    TRUE_FALSE = "true_false"  # 확인
    TECHNICAL = "technical"


class QuizLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Quiz(BaseModel):
    question: str
    options: Optional[List[str]] = None
    correct_answer: str
    quiz_type: QuizType
    level: QuizLevel
    acceptable_variations: List[str] = []
    evaluation_criteria: Dict[str, float] = {}


class QuizResponse(BaseModel):
    notes: str
    quizzes: List[Quiz]
