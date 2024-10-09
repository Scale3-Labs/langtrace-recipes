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




if __name__ == "__main__":
    yoda_speak()
