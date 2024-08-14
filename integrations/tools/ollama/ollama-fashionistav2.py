# Install the required packages: streamlit, langtrace-python-sdk, ollama

# pip install streamlit langtrace-python-sdk ollama

# You can run this script with: streamlit run ollama-fashionistav2.py.py


import streamlit as st
from langtrace_python_sdk import langtrace, with_langtrace_root_span
import ollama

# Initialize Langtrace
langtrace.init(api_key='YOUR_API_KEY', write_spans_to_console=False)

@with_langtrace_root_span()
def generate_response(prompt):
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']

@with_langtrace_root_span()
def give_fashion_advice(event_type):
    prompt = f"You are an AI assistant with expertise in men's clothing. Help me pick clothing for a {event_type}. Don't ask any follow-up questions."
    return generate_response(prompt)

# Streamlit interface
st.title("👔 Fashionista bot: AI Fashion Advisor")
st.write("Get clothing recommendations for various events using Llama 3.1 via Ollama.")

event_type = st.text_input("Enter the type of event (e.g., casual Friday, business meeting):")

if st.button("Get Advice"):
    if event_type:
        with st.spinner("Generating advice..."):
            advice = give_fashion_advice(event_type)
        st.write(advice)
    else:
        st.warning("Please enter an event type.")

# Add a sidebar with additional information
st.sidebar.header("About")
st.sidebar.write("This app uses Llama 3.1 running locally via Ollama to provide fashion advice for events.")
st.sidebar.write("It's integrated with Langtrace for observability.")

