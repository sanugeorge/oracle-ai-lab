import ollama

reply = ollama.chat(
    model="gemma4:e4b",
    messages=[{"role": "user", "content": "What is a foreign key? Two sentences."}],
)
print(reply["message"]["content"])