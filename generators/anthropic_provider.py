from .base import BaseProvider

class AnthropicProvider(BaseProvider):
    def __init__(self, model, api_key=None):
        self.model = model
        self.api_key = api_key

    def generate(self, prompt):
        # TODO: Implémenter l'appel API Anthropic
        return []
