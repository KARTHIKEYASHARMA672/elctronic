import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "meta-llama/llama-3-8b-instruct",
    "messages": [{"role": "user", "content": "Hello"}]
}

r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
print(r.status_code, r.text)
