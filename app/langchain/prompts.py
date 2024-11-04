# app/langchain/prompts.py
from langchain_core.prompts import PromptTemplate

note_prompt = PromptTemplate(
    input_variables=["text"],
    template="다음 텍스트를 기반으로 핵심 학습 노트를 요약해 주세요:\n\n{text}"
)

quiz_prompt = PromptTemplate(
    input_variables=["notes"],
    template="이 학습 노트를 기반으로 객관식, 서술형, 빈칸 채우기 유형의 퀴즈 5개와 그 정답을 생성해 주세요:\n\n{notes}"
)
