from langchain.callbacks.base import AsyncCallbackHandler
import tiktoken

def count_tokens(text: str, model_name: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

class TokenUsageCallbackHandler(AsyncCallbackHandler):
    def __init__(self):
        self.token_usage = {}

    async def on_llm_end(self, response, **kwargs):
        print(f"LLM output: {response.llm_output}")
        if response.llm_output:
            # OpenAI API의 응답에서 토큰 사용량 추출
            token_usage = response.llm_output.get('token_usage')
            if not token_usage and 'additional_kwargs' in response.llm_output:
                token_usage = response.llm_output['additional_kwargs'].get('token_usage')
            if token_usage:
                self.token_usage = token_usage
