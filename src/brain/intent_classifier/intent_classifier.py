import json

from jinja2 import Environment, BaseLoader

from src.llms import LLM

INSTRUCTION = open("src/brain/intent_classifier/instruction.jinja2").read().strip()


class IntentClassifier:
    def __init__(self, model: str):
        self.llm = LLM(model_id=model)

    def combine(self, prompt):
        env = Environment(loader=BaseLoader())
        template = env.from_string(INSTRUCTION)
        # TODO: add prompt context to the INSTRUCTION using 'prompt_context'
        return template.render(user_prompt=prompt)

    def validate_response(self, response: str):
        response = response.strip().replace("```json", "```")

        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()

        try:
            response = json.loads(response)
        except Exception as _:
            return False

        response = {k.replace("\\", ""): v for k, v in response.items()}

        if "module" not in response:
            return False
        else:
            response["intent"] = 'get' if 'get' in response.get('intent', '').lower() or 'set' in response.get('intent', '').lower() else 'none'
            return response

    def execute(self, prompt: str) -> str:
        inference_prompt = self.combine(prompt)
        response = self.llm.inference(inference_prompt)

        if response == "LLM not working.":
            return response

        valid_response = self.validate_response(response)

        while not valid_response:
            print("Invalid response from the intent model, trying again...")
            return self.execute(prompt)

        return valid_response
