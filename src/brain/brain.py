from .assistant import Assistant
from .intent_classifier import IntentClassifier
from src.config import Config


class Brain:
    def __init__(self):
        self.base_model = Config().get_model()
        self.intent_classifier = IntentClassifier(model=self.base_model)
        self.assistant = Assistant(model=self.base_model)
        self.modules = {
            # "Image Generation Module": ImageGenerationModuleClass,
            # "Selfie Generation Module": SelfieGenerationModuleClass,
            # "Google Task Module": GoogleTaskModuleClass,
            # "Web Summarizer Module": WebSummarizerModuleClass
        }

    def execute(self, prompt: str, user_name: str) -> str:
        intent = self.intent_classifier.execute(prompt=prompt)

        if intent == "LLM not working.":
            return f"Connection to {Config().get_llm_type()} service failed. Check if {Config().get_llm_type()} is running."

        print(f"Intent classified: {intent}")

        module_name = intent.get("module")

        # Get the corresponding class
        additional_module = self.modules.get(module_name)

        # call modules
        if additional_module:
            # Instantiate the class and call its method
            result = additional_module.execute(prompt)
            print(f"Additional module response: {result}")

        # inference for response
        response = self.assistant.execute(prompt, user_name, '')

        return response
