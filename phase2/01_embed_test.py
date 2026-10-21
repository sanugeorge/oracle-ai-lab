import ollama

result = ollama.embed(model="embeddinggemma", input=["What is a primary key?"])
vec = result["embeddings"][0]
print("Dimensions:", len(vec))
print("First 5 numbers:", vec[:5])

result = ollama.embed(model="embeddinggemma", input=["Where is my key?"])
print("Second 4 numbers:", vec[:4])


