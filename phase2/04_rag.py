import os
import sys
import array
from pathlib import Path
import ollama
import oracledb
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CHAT_MODEL = "gemma4:e4b"
EMBED_MODEL = "embeddinggemma"

def get_connection():
    return oracledb.connect(
        user=os.getenv("ORA_USER"),
        password=os.getenv("ORA_PASSWORD"),
        dsn=os.getenv("ORA_DSN"),
    )

def retrieve(question, k=3):
    q_vec = ollama.embed(model=EMBED_MODEL, input=[question])["embeddings"][0]
    sql = """
        SELECT id, title, content, VECTOR_DISTANCE(embedding, :q, COSINE) AS distance
        FROM docs
        ORDER BY distance
        FETCH FIRST :k ROWS ONLY
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"q": array.array("f", q_vec), "k": k})
            return cur.fetchall()

question = " ".join(sys.argv[1:]) or "my queries are slow"
rows = retrieve(question)

context = "\n".join(f"[{id}] {title}: {content}" for id, title, content, _ in rows)

messages = [
    {
        "role": "system",
        "content": (
            "Answer the question using ONLY the context provided. "
            "If the context does not contain the answer, say you don't know. "
            "Cite the source ids in square brackets, like [3]."
        ),
    },
    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
]

print(f"Question: {question}\n")
print("Retrieved:")
for id, title, _, distance in rows:
    print(f"  [{id}] {title} ({distance:.3f})")

print("\nAnswer: ", end="", flush=True)
for chunk in ollama.chat(model=CHAT_MODEL, messages=messages,
                         options={"temperature": 0.1}, stream=True):
    print(chunk["message"]["content"], end="", flush=True)
print()