from .ollama_provider import Ollama
from ..brain.memory.memory import Memory
from ..utils import get_current_time, get_system_prompt


class LLM:
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.memory = Memory()

    def inference(self, prompt: str) -> str:
        response = Ollama().inference(self.model_id, prompt).strip()
        return response

    def chat(self, prompt: str, user_name: str):
        interactions = self.memory.get_interactions(10)
        system_interactions = get_system_prompt(user_name)

        messages = []

        # Add system_instructions to messages
        messages.extend(system_interactions)

        # Add conversations to messages
        for interaction in interactions:
            messages.append({"role": interaction.role, "content": interaction.content})

        messages.append({'role': 'user', 'content': prompt})

        self.memory.add_interaction('user', prompt, None, get_current_time())

        response = Ollama().chat(self.model_id, messages)
        llm_response = response['message']['content']
        self.memory.add_interaction('assistant', llm_response, None, get_current_time())
        return llm_response
