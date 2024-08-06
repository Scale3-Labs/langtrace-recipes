### 1. Create a python virtual environment. 
Lets call our virtual enviornment chatbot but you can name it whatever you like.


```
python3 -m venv chatbot

```

You should now have a directory called chatbot after running this command.

### 2. Activate virtual enviornment

```
source chatbot/bin/activate

```

### 3. Install all requirements

```
pip install -r requirements.txt
```

### 4. Add the LANGTRACE_API_KEY to your environment variables

```
export LANGTRACE_API_KEY=<your-api-key>
```

### 5. Initialize Langtrace in your project. Make sure to replace the YOUR_LANGTRACE_API_KEY placeholder with your actual API key. 
![Langtrace Init](../assets/langtrace_init.png)

### 6. Run your chatbot 

```
python3 main.py
```