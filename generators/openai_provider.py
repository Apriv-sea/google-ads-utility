import openai
from config.settings import OPENAI_API_KEY
from .base import BaseProvider

openai.api_key = OPENAI_API_KEY

class OpenAIProvider(BaseProvider):
    def __init__(self, model):
        self.model = model

    def generate(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"user","content":prompt}]
        )
        text = response.choices[0].message.content
        return text.split("\n")
