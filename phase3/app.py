import os
import array
from pathlib import Path

import ollama
import oracledb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CHAT_MODEL = "gemma4:e4b"
EMBED_MODEL = "embeddinggemma"
MAX_DISTANCE = 0.7  # above this, we treat the match as irrelevant

app = FastAPI(title="Oracle RAG API")


def get_connection():
    return oracledb.connect(
        user=os.getenv("ORA_USER"),
        password=os.getenv("ORA_PASSWORD"),
        dsn=os.getenv("ORA_DSN"),
    )


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    k: int = Field(default=3, ge=1, le=10)


def retrieve(question: str, k: int):
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/documents")
def documents():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title FROM docs ORDER BY id")
            return [{"id": i, "title": t} for i, t in cur]


@app.post("/ask")
def ask(req: AskRequest):
    try:
        rows = retrieve(req.question, req.k)
    except oracledb.Error as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")

    sources = [
        {"id": i, "title": t, "distance": round(d, 3)} for i, t, _, d in rows
    ]

    if not rows or rows[0][3] > MAX_DISTANCE:
        return {"answer": "No relevant documents found.", "sources": sources}

    context = "\n".join(f"[{i}] {t}: {c}" for i, t, c, _ in rows)
    messages = [
        {
            "role": "system",
            "content": (
                "Answer using ONLY the context provided. If the context does "
                "not contain the answer, say you don't know. "
                "Cite source ids in square brackets, like [3]."
            ),
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {req.question}"},
    ]

    try:
        reply = ollama.chat(model=CHAT_MODEL, messages=messages,
                            options={"temperature": 0.1})
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Model error: {e}")

    return {"answer": reply["message"]["content"], "sources": sources}