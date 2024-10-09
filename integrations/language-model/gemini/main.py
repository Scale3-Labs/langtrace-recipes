"""
This script demonstrates how to use the Gemini API for language model tasks.
"""

import pathlib
from langtrace_python_sdk import langtrace
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
langtrace.init()
genai.configure()


def yoda_speak():
    """
    Generate a response in Yoda-speak.
    """
    model = genai.GenerativeModel(
        "gemini-1.5-pro", system_instruction="Respond only in Yoda-speak."
    )

    response = model.generate_content("Write a story about a AI and magic", stream=True)
    for res in response:
        if res.text:
            print(res.text)


def image_to_text():
    """
    Generate a text description of an image.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    image1 = {
        "mime_type": "image/jpeg",
        "data": pathlib.Path("assets/panda.jpg").read_bytes(),
    }

    prompt = "Describe me this picture. What do you see in it."
    response = model.generate_content([prompt, image1], stream=True)
    for res in response:
        print(res.text)


if __name__ == "__main__":
    yoda_speak()
    image_to_text()
