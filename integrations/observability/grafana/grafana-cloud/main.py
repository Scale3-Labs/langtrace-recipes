import os
from langtrace_python_sdk import langtrace
from groq import Groq


langtrace.init(api_key="YOUR_LANGTRACE_API_KEY")
class StoryGenerator:
    def __init__(self, model="llama3-8b-8192", temperature=1, max_tokens=1024, top_p=1, stream=True, stop=None):
        self.client = Groq(
                           api_key="YOUR_API_KEY"
                           )
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.stream = stream
        self.stop = stop

    def generate_story(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            stream=self.stream,
            stop=self.stop,
        )

        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")

# Usage example:
if __name__ == "__main__":
    print("test")
    generator = StoryGenerator()
    print("test2")
    generator.generate_story("write me a short story")