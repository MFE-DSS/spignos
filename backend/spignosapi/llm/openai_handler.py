import os
from openai import OpenAI

openai_api_key = os.environ.get("OPENAI_API_KEY")


class OpenAIHandler:
    def __init__(self):
        self.api_key = openai_api_key
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt, max_tokens=256, temperature=0.7, model="gpt-4"):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Tu es un assistant intelligent."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[ERREUR OpenAI] {str(e)}"
