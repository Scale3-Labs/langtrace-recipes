from langtrace_python_sdk import langtrace
langtrace.init("YOUR_LANGTRACE_API_KEY")#must precede any llm imports
## ENSURE TO REPLACE THE YOUR_LANGTRACE_API_KEY LITERAL WITH YOUR ACTUAL API KEY WHICH YOU GENEREATED IN LANGTRACE.Ai

import sys
from termcolor import colored, cprint
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def handle_conversation():
    print("Welcome to the AI Chatbot! Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: \n")
       
        if user_input.lower() == "exit":   
            break
       
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="gpt-3.5-turbo",
        )
        

        print (colored("\nBot: ","red"), colored(chat_completion.choices[0].message.content , "red"))
    

if __name__ == "__main__":
    handle_conversation()
