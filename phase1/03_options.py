import ollama

MODEL = "gemma4:e4b"

messages = [
    {"role":"system", "content":"You are a experianced DBA.answer briefly and practically."},
    {"role":"user","content":"How do i find slow SQL in Oracle?"},
]

stream = ollama.chat(
    model=MODEL,
    messages={"temperature":0.2},
    stream=True,
)


for chunk in stream:
    print(chunk["messages"]["content"],end="", flush=True)
print()