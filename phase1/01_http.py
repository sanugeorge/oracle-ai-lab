import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "gemma4:e4b",
        "messages": [{"role": "user", "content": "What is a foreign key? Two sentences."}],
        "stream": False,
    },
    timeout=300,
)

print("Status code:", response.status_code)
data = response.json()
print(data["message"]["content"])