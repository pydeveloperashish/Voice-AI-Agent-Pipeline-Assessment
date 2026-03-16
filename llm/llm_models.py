import json
from dotenv import load_dotenv

load_dotenv()

class BaseLLM:
    def generate(self, prompt: str) -> dict:
        raise NotImplementedError
    


# Openai GPT-4o-Mini Implementation
from openai import OpenAI
class OpenAILLM(BaseLLM):

    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
    


# Openai Ollama Model Implementation
import json
import ollama

class OllamaLLM(BaseLLM):
    MODEL_NAME = "lfm2.5-thinking:latest"

    def __init__(self, model = MODEL_NAME):
        self.model = model

        installed_models = [m.model for m in ollama.list().models]
        if self.model not in installed_models:
            print(f"{self.model} model not found. Pulling model: {self.model}...")
            ollama.pull(self.model)
            print("Model {self.model} Downloaded")
        print(f"Model Found: {self.model}")

    def generate(self, prompt: str) -> dict:
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        output_text = response["message"]["content"].strip()

        try:
            return json.loads(output_text)

        except json.JSONDecodeError:
            return {
                "intent": "unclear",
                "action": "unclear",
                "confidence": 0.0,
                "notes": "Failed to parse Ollama response"
            }