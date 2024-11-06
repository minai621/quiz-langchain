import time
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Tuple, Any, Callable
from langchain_openai import ChatOpenAI
from app.models.quiz_models import Quiz
from app.services.translation_service import TranslationService
from app.config.settings import settings
from app.langchain.prompts import SUMMARY_PROMPT, QUIZ_PROMPT
import json
import re
from langchain.callbacks.manager import AsyncCallbackManager
from app.utils.token_usage_callback_handler import TokenUsageCallbackHandler, count_tokens

@dataclass
class ProcessingStep:
    """각 처리 단계의 정보를 저장하는 데이터 클래스"""
    name: str
    input_text: str
    output_text: str
    error: Optional[str] = None
    duration: float = 0
    token_usage: Optional[dict] = None  # 토큰 사용량 추가

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7,
            openai_api_key=settings.openai_api_key,
            verbose=True,  
            max_retries=3,
            request_timeout=120
        )
        self.translation_service = TranslationService()
        self.processing_steps = []

        # 난이도 매핑
        self.level_mapping = {
            "고급": "high", "중급": "medium", "초급": "low",
            "상": "high", "중": "medium", "하": "low",
            "HIGH": "high", "MEDIUM": "medium", "LOW": "low"
        }

        # 퀴즈 유형 매핑
        self.type_mapping = {
            "객관식": "multiple_choice", 
            "단답형": "short_answer",  
            "참/거짓": "true_false", "참거짓": "true_false",
            "다중 선택": "multiple_choice",
            "MULTIPLE_CHOICE": "multiple_choice",
            "SHORT_ANSWER": "short_answer",
            "TRUE_FALSE": "true_false"
        }

    async def process_document(
    self,
    text: str,
    exists_quizzes: List[Quiz]
) -> Tuple[str, List[Quiz]]:
        """문서 처리의 메인 파이프라인"""
        try:
            # 1. 텍스트 요약
            summary = await self._process_step(
                "요약 생성",
                lambda: self.llm.ainvoke(SUMMARY_PROMPT.format(text=text)),
                is_llm_call=True,
                input_text=SUMMARY_PROMPT.format(text=text)
            )
            
            existing_quiz_text = json.dumps([quiz.model_dump() for quiz in exists_quizzes])
            quiz_prompt = QUIZ_PROMPT.format(
                text=summary,
                existing_quizzes=existing_quiz_text
            )
            quiz_response = await self._process_step(
                "퀴즈 생성",
                lambda: self.llm.ainvoke(quiz_prompt),
                is_llm_call=True,
                input_text=quiz_prompt
            )
            
            quiz = await self._process_step(
                "레이블 보호",
                lambda: self._sync_protect_labels(quiz_response),
                input_text=quiz_response
            )
            
            ko_quiz = await self._process_step(
                "한글 번역",
                lambda: self.translation_service.translate(quiz, 'KO'),
                is_translation=True,
                input_text=quiz
            )

            
            restored_quiz = await self._process_step(
                "레이블 복원",
                lambda: self._sync_restore_labels(ko_quiz),
                input_text=ko_quiz
            )
            
            parsed_quizzes = await self._process_step(
                "퀴즈 파싱",
                lambda: self._parse_quizzes(restored_quiz),
                input_text=restored_quiz
            )

            return summary, parsed_quizzes

        except Exception as e:
            self.processing_steps.append(
                ProcessingStep(
                    name="오류 발생",
                    input_text=str(e),
                    output_text="",
                    error=str(e)
                )
            )
            raise e


    async def _process_step(self, step_name: str, process_func: Callable, is_llm_call=False, is_translation=False, input_text='') -> Any:
        """Helper method to track and record each processing step."""
        try:
            start_time = time.time()
            token_usage = {}
            result = None

            if is_llm_call:
                # LLM call handling
                callback_handler = TokenUsageCallbackHandler()
                callback_manager = AsyncCallbackManager([callback_handler])
                self.llm.callback_manager = callback_manager

                result = await process_func()
                result_text = result.content if hasattr(result, 'content') else str(result)
                token_usage = callback_handler.token_usage or {}
                print(f"Debug - Token usage for {step_name}: {token_usage}")
            else:
                # Properly await process_func if it's a coroutine
                if asyncio.iscoroutinefunction(process_func):
                    result = await process_func()
                else:
                    result = process_func()

                # If result is a coroutine, await it
                if asyncio.iscoroutine(result):
                    result = await result

                result_text = result

                if is_translation:
                    # Ensure result_text is a string
                    if not isinstance(result_text, str):
                        raise TypeError(f"Expected result_text to be a string in step '{step_name}', but got {type(result_text)}")
                    # Token count
                    input_tokens = count_tokens(input_text)
                    output_tokens = count_tokens(result_text)
                    token_usage = {
                        'prompt_tokens': input_tokens,
                        'completion_tokens': output_tokens,
                        'total_tokens': input_tokens + output_tokens
                    }

            end_time = time.time()

            self.processing_steps.append(
                ProcessingStep(
                    name=step_name,
                    input_text=str(input_text),
                    output_text=str(result_text),
                    duration=end_time - start_time,
                    token_usage=token_usage
                )
            )

            return result_text

        except Exception as e:
            self.processing_steps.append(
                ProcessingStep(
                    name=step_name,
                    input_text=str(input_text),
                    output_text="",
                    error=str(e),
                    duration=0
                )
            )
            raise e

    def _parse_quizzes(self, quiz_text: str) -> List[Quiz]:
        """퀴즈 텍스트를 파싱하여 Quiz 객체 리스트로 변환"""
        quizzes = []
        current_quiz = {}
        lines = quiz_text.split('\n')

        for line in lines:
            line = line.strip()
            if not line or line == '---':
                if self._is_valid_quiz(current_quiz):
                    try:
                        quizzes.append(Quiz(**current_quiz))
                    except Exception as e:
                        print(f"Quiz parsing error: {e}, Quiz data: {current_quiz}")
                    current_quiz = {}
                continue

            # 레이블과 값을 정규표현식으로 추출
            for label in ['LEVEL', 'TYPE', 'QUESTION', 'OPTIONS', 'ANSWER', 
                         'ACCEPTABLE_VARIATIONS', 'EVALUATION_CRITERIA']:
                match = re.match(f'^{label}: ?(?P<value>.+)$', line)
                if match:
                    value = match.group('value').strip()
                    self._process_quiz_field(current_quiz, label, value)
                    break

        # 마지막 퀴즈 처리
        if self._is_valid_quiz(current_quiz):
            try:
                quizzes.append(Quiz(**current_quiz))
            except Exception as e:
                print(f"Quiz parsing error: {e}, Quiz data: {current_quiz}")

        return quizzes

    def _is_valid_quiz(self, quiz: dict) -> bool:
        """퀴즈 데이터가 유효한지 검증"""
        required_fields = {'question', 'correct_answer', 'quiz_type', 'level'}
        return all(field in quiz for field in required_fields)

    def _process_quiz_field(self, quiz: dict, label: str, value: str) -> None:
        """퀴즈 필드 처리"""
        if label == 'LEVEL':
            mapped_level = self.level_mapping.get(value.strip())
            if mapped_level:
                quiz['level'] = mapped_level
            else:
                print(f"Unknown level: {value}")
        
        elif label == 'TYPE':
            mapped_type = self.type_mapping.get(value.strip())
            if mapped_type:
                quiz['quiz_type'] = mapped_type
            else:
                print(f"Unknown type: {value}")
        
        elif label == 'QUESTION':
            quiz['question'] = value
        
        elif label == 'OPTIONS':
            quiz['options'] = [opt.strip() for opt in value.split('|')]
        
        elif label == 'ANSWER':
            quiz['correct_answer'] = value
            
        elif label == 'ACCEPTABLE_VARIATIONS':
            quiz['acceptable_variations'] = [v.strip() for v in value.split('|')]
            
        elif label == 'EVALUATION_CRITERIA':
            if value.strip():
                criteria_pairs = [pair.strip() for pair in value.split(',')]
                criteria_dict = {}
                for pair in criteria_pairs:
                    if ':' in pair:
                        k, v = pair.split(':', 1)
                        try:
                            criteria_dict[k.strip()] = float(v.strip())
                        except ValueError:
                            print(f"Invalid value for criterion '{k}': '{v}'")
                    else:
                        print(f"Invalid criterion format: '{pair}'")
                quiz['evaluation_criteria'] = criteria_dict
            else:
                quiz['evaluation_criteria'] = {}


    def _sync_protect_labels(self, text: str) -> str:
        """동기 버전의 레이블 보호 함수"""
        return self.protect_labels(text)

    def _sync_restore_labels(self, text: str) -> str:
        """동기 버전의 레이블 복원 함수"""
        return self.restore_labels(text)

    def protect_labels(self, text: str) -> str:
        """번역 시 레이블 보호를 위한 XML 태그 추가"""
        labels = ['LEVEL', 'TYPE', 'QUESTION', 'OPTIONS', 'ANSWER']
        for label in labels:
            text = text.replace(f"{label}:", f"<{label}>:")
        return text

    def restore_labels(self, text: str) -> str:
        """번역 후 레이블 복원"""
        labels = ['LEVEL', 'TYPE', 'QUESTION', 'OPTIONS', 'ANSWER']
        for label in labels:
            text = text.replace(f"<{label}>:", f"{label}:")
        return text

    def get_processing_history(self) -> List[ProcessingStep]:
        """처리 단계별 히스토리 반환"""
        return self.processing_steps
