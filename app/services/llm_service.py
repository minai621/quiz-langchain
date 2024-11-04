# app/services/llm_service.py
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import os
from typing import Tuple, List
from app.models.quiz_models import Quiz

class LLMService:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set!")
            
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        self.template = """Create detailed notes from the following text and generate 5 multiple choice questions:
        
        Text: {text}
        
        Format the output as follows:
        Notes:
        [Your detailed notes here]
        
        Questions:
        1. [Question]
        A) [Option]
        B) [Option]
        C) [Option]
        D) [Option]
        Correct Answer: [A/B/C/D]
        
        [Repeat for all 5 questions]
        """
        
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template=self.template
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_notes_and_quizzes(self, text: str) -> Tuple[str, List[Quiz]]:
        """텍스트로부터 노트와 퀴즈를 생성하는 메서드"""
        result = self.chain.invoke({"text": text})
        output = result['text']
        
        # Notes 부분 추출
        notes_match = re.search(r'Notes:(.*?)Questions:', output, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ""
        
        # Questions 부분 추출 및 파싱
        questions_match = re.search(r'Questions:(.*)', output, re.DOTALL)
        questions_text = questions_match.group(1).strip() if questions_match else ""
        
        quizzes = self._parse_questions(questions_text)
        return notes, quizzes
        
    def _parse_questions(self, questions_text: str) -> List[Quiz]:
        """질문 텍스트를 파싱하여 Quiz 객체 리스트로 변환하는 메서드"""
        quizzes = []
        current_question = {}
        
        for line in questions_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if re.match(r'^\d+\.', line):
                if current_question:
                    quizzes.append(Quiz(**current_question))
                current_question = {
                    "question": line.split('. ', 1)[1],
                    "options": []
                }
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                current_question["options"].append(line[2:].strip())
            elif line.startswith('Correct Answer:'):
                current_question["correct_answer"] = line.split(': ')[1].strip()
        
        if current_question:
            quizzes.append(Quiz(**current_question))
            
        return quizzes
