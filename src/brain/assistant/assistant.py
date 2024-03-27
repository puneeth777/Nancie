import json

from jinja2 import Environment, BaseLoader

from src.llms import LLM

INSTRUCTION = open("src/brain/assistant/instruction.jinja2").read().strip()


class Assistant:
    def __init__(self, model: str):
        self.llm = LLM(model_id=model)

    def combine(self, prompt: str, context: str):
        env = Environment(loader=BaseLoader())
        template = env.from_string(INSTRUCTION)
        # TODO: add prompt context to the INSTRUCTION using 'prompt_context'
        return template.render(user_prompt=prompt, prompt_context=context)

    def execute(self, prompt: str, user_name: str, context: str) -> str:
        inference_prompt = self.combine(prompt, context)
        response = self.llm.chat(prompt, user_name)

        if response == "LLM not working.":
            return response

        return response