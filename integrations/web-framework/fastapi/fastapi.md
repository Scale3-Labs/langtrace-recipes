
## Overview

FastAPI is a modern web framework for building APIs with Python 3.6+ based on standard Python type hints. Langtrace can be easily integrated with FastAPI applications with the help of the Langtrace SDK.

## Steps

Follow the steps below to integrate Langtrace with your FastAPI application:

- Install the Langtrace SDK in your project and initialize it. See the example below:

```python Python
from fastapi import FastAPI
from langtrace_python_sdk import langtrace
from openai import OpenAI

langtrace.init(api_key="<LANGTRACE_API_KEY>")
app = FastAPI()
client = OpenAI()

@app.get("/")
def root():
    client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say this is a test three times"}],
        stream=False,
    )
    return {"Hello": "World"}
```
