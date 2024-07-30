
from langtrace_python_sdk import langtrace
langtrace.init("YOUR_LANGTRACE_API_KEY") #must precede any llm imports

import sys
from termcolor import colored, cprint
from openai import OpenAI

import os
os.environ["COHERE_API_KEY"] = "YOUR_COHERE_API_KEY"

import cohere

co = cohere.Client(
    api_key=os.environ["COHERE_API_KEY"],
)


def handle_conversation():
    
    context = ""
    print("Welcome to the AI Chatbot! Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: \n")
       
        if user_input.lower() == "exit":
            
            break

        chat = co.chat(
        message=user_input,)
        

        print (colored("\nBot: ","red"), colored(chat.text , "red"))
    

if __name__ == "__main__":
    handle_conversation()
