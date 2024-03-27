import httpx
import ollama
from httpx import ConnectError


class Ollama:
    def inference(self, model_id: str, prompt: str) -> str:
        try:
            response = ollama.generate(
                model=model_id,
                prompt=prompt.strip()
            )
            return response['response']
        except ConnectError as e:
            return "LLM not working."

    def chat(self, model_id: str, messages):
        try:
            response = ollama.chat(
                model=model_id,
                messages=messages
            )
            return response
        except ConnectError as e:
            return "LLM not working."
