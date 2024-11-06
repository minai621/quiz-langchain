import deepl
import os
from langdetect import detect
from app.config.settings import settings
from langchain_openai import ChatOpenAI

class TranslationService:
    def __init__(self):
        self.deepl_translator = deepl.Translator(settings.deepl_api_key)
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.1,
            openai_api_key=settings.openai_api_key
        )

    async def translate(self, text: str, target_lang: str = 'EN-US') -> str:
        try:        
            # DeepL 번역 시도
            result = self.translator.translate_text(
                text,
                target_lang=target_lang,
                tag_handling='xml',
                ignore_tags=['LEVEL', 'TYPE', 'QUESTION', 'OPTIONS', 'ANSWER']
            )
            return result.text
        
        except Exception as e:
            # DeepL 실패시 GPT 사용
            prompt = f"Translate the following text to {'English' if target_lang.startswith('EN') else 'Korean'}. Maintain accuracy and preserve any technical terms:\n\n{text}"
            response = await self.llm.ainvoke(prompt)
            return response.content
