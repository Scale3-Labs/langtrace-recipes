import config
from typing import List
from groq import Groq
from openai import OpenAI
from ollama import generate


class LLMService:
    def __init__(self):
        self.provider = config.LLM_PROVIDER
        if self.provider == 'groq':
            self.client = Groq(api_key=config.GROQ_API_KEY)
        elif self.provider == 'openai':
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def generate_explanation(self, prompt: str) -> str:
        if self.provider == 'groq':
            return self._generate_groq(prompt)
        elif self.provider == 'openai':
            return self._generate_openai(prompt)
        elif self.provider == 'ollama':
            return self._generate_ollama(prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _generate_groq(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    def _generate_openai(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def _generate_ollama(self, prompt: str) -> str:
        response_text = ""
        for part in generate(model=config.LLM_MODEL, prompt=prompt, stream=True):
            if 'response' in part:
                response_text += part['response']
        return response_text.strip()
