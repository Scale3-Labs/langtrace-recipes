

## Steps

Follow the steps below to integrate Langtrace with your Flask application:

- Install the Langtrace SDK in your project and initialize it inside the **app.py** file:

```python Python
from flask import Flask
from langtrace_python_sdk import langtrace
from openai import OpenAI

langtrace.init()
client = OpenAI()
app = Flask(__name__)


@app.route("/")
def main():
    client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say this is a test three times"}],
        stream=False,
    )
    return "Hello, World!"
```
