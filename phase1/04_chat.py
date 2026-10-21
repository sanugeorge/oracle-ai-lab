import ollama

MODEL = "gemma4:e4b"

messages = [
    {"role": "system", "content": "You are a helpful Oracle and Python tutor. Keep answers short."}
]

print("Chat with Gemma 4. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("quit", "exit"):
        break
    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    print("Gemma: ", end="", flush=True)
    reply = ""
    for chunk in ollama.chat(model=MODEL, messages=messages, options={"temperature": 0.3}, stream=True):
        piece = chunk["message"]["content"]
        reply += piece
        print(piece, end="", flush=True)
    print("\n")

    messages.append({"role": "assistant", "content": reply})