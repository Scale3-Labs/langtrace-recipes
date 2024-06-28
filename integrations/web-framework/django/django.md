

## Steps

Follow the steps below to integrate Langtrace with your Django application:

- Install the Langtrace SDK. Initialize django project and add this inside the **init.py** file, for the sake of example we added the following lines in `settings.py` file.

```python
# settings.py
from langtrace_python_sdk import langtrace
langtrace.init(api_key="<YOUR_API_KEY>")
```

This is a sample `views.py` file that uses the Langtrace SDK to call the OpenAI API:

```python Python
# Create your views here.
from django.http import HttpResponse
from openai import OpenAI


def call_openai():
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say this is a test three times"}],
        stream=False,
    )
    return str(response.choices[0].message.content)


def index(request):
    return HttpResponse(call_openai())
```
