import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
EMBEDDING_MODEL = 'all-mpnet-base-v2'
DIMENSION = 768
MAX_TOKENS = 7000
CHUNK_SIZE = 500
MAX_ATTEMPTS = 3

LLM_PROVIDER = 'openai' # 'groq','openai',or 'ollama'
LLM_MODEL = 'llama3.1'  # for ollama only
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

