import json
from model_selector import get_title_prompt, get_desc_prompt
import openai

def parse_llm_output(text, expected_length):
    try:
        items = json.loads(text)
        if isinstance(items, list) and len(items) == expected_length:
            return items
    except json.JSONDecodeError:
        return None
    return None

def generate_ads(context, provider, model, api_key):
    if provider == "OpenAI":
        openai.api_key = api_key
        prompt = get_title_prompt(context)
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return parse_llm_output(response.choices[0].message.content, expected_length=5)