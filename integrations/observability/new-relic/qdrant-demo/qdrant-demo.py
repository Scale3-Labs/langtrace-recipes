import os
import time
import openai
from qdrant_client import QdrantClient
from langtrace_python_sdk import langtrace, with_langtrace_root_span
from typing import List, Dict, Any
from dotenv import load_dotenv
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Load environment variables from .env file
load_dotenv()

# Configure the OTLP exporter to use the correct endpoint and API key
otlp_endpoint = "https://otlp.nr-data.net"
otlp_exporter = OTLPSpanExporter(
    endpoint=otlp_endpoint,
    headers=(("Content-Type", "application/json"),))

# Initialize environment and clients
openai_api_key = os.getenv("OPENAI_API_KEY")
langtrace_api_key = os.getenv("LANGTRACE_API_KEY")

if not openai_api_key or not langtrace_api_key:
    raise ValueError("OPENAI_API_KEY or LANGTRACE_API_KEY not found in .env file")

openai_client = openai.Client(api_key=openai_api_key)
langtrace.init(api_key=langtrace_api_key, custom_remote_exporter=otlp_exporter)
qdrant_client = QdrantClient(":memory:") 

@with_langtrace_root_span("initialize_knowledge_base")
def initialize_knowledge_base(documents: List[str]) -> None:
    try: 
        qdrant_client.add(
            collection_name="knowledge-base",
            documents=documents
        )
        print(f"Knowledge base initialized with {len(documents)} documents")
    except Exception as e:
        print(f"Error initializing knowledge base: {str(e)}")
        

@with_langtrace_root_span("query_vector_db")
def query_vector_db(question: str, n_points: int = 3) -> List[Dict[str, Any]]:
    results = qdrant_client.query(
        collection_name="knowledge-base",
        query_text=question,
        limit=n_points,
    )
    print(f"Vector DB queried, returned {len(results)} results")
    return results

@with_langtrace_root_span("generate_llm_response")
def generate_llm_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        timeout=10.0,
    )
    response = completion.choices[0].message.content
    print(f"LLM response generated")
    return response

@with_langtrace_root_span("rag")
def rag(question: str, n_points: int = 3) -> str:
    print(f"Processing RAG for question: {question}")
    
    context = "\n".join([r.document for r in query_vector_db(question, n_points)])
    metaprompt = f"""
    You are a software architect.
    Answer the following question using the provided context.
    If you can't find the answer, do not pretend you know it, but answer "I don't know".

    Question: {question.strip()}

    Context:
    {context.strip()}

    Answer:
    """    
    answer = generate_llm_response(metaprompt)
    print(f"RAG completed, answer length: {len(answer)} characters")
    return answer

def demonstrate_different_queries():
    questions = [
        "What is Qdrant used for?",
        "How does Docker help developers?",
        "What is the purpose of MySQL?",
        "Can you explain what FastAPI is?",
    ]
    for question in questions:
        try:
            answer = rag(question)
            print(f"Question: {question}")
            print(f"Answer: {answer}\n")
        except Exception as e:
            print(f"Error processing question '{question}': {str(e)}\n")

if __name__ == "__main__":
    # Initialize knowledge base
    documents = [
        "Qdrant is a vector database & vector similarity search engine. It deploys as an API service providing search for the nearest high-dimensional vectors. With Qdrant, embeddings or neural network encoders can be turned into full-fledged applications for matching, searching, recommending, and much more!",
        "Docker helps developers build, share, and run applications anywhere — without tedious environment configuration or management.",
        "PyTorch is a machine learning framework based on the Torch library, used for applications such as computer vision and natural language processing.",
        "MySQL is an open-source relational database management system (RDBMS). A relational database organizes data into one or more data tables in which data may be related to each other; these relations help structure the data. SQL is a language that programmers use to create, modify and extract data from the relational database, as well as control user access to the database.",
        "NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server. NGINX is known for its high performance, stability, rich feature set, simple configuration, and low resource consumption.",
        "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
        "SentenceTransformers is a Python framework for state-of-the-art sentence, text and image embeddings. You can use this framework to compute sentence / text embeddings for more than 100 languages. These embeddings can then be compared e.g. with cosine-similarity to find sentences with a similar meaning. This can be useful for semantic textual similar, semantic search, or paraphrase mining.",
        "The cron command-line utility is a job scheduler on Unix-like operating systems. Users who set up and maintain software environments use cron to schedule jobs (commands or shell scripts), also known as cron jobs, to run periodically at fixed times, dates, or intervals.",
    ]
    initialize_knowledge_base(documents)

    demonstrate_different_queries()