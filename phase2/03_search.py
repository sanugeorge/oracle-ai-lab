import os
import sys
import array
from pathlib import Path
import ollama
import oracledb
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

def get_connection():
    return oracledb.connect(
        user=os.getenv("ORA_USER"),
        password=os.getenv("ORA_PASSWORD"),
        dsn=os.getenv("ORA_DSN"),
    )

question = " ".join(sys.argv[1:]) or "my queries are slow"

q_vec = ollama.embed(model="embeddinggemma", input=[question])["embeddings"][0]

sql = """
    SELECT title, content, VECTOR_DISTANCE(embedding, :q, COSINE) AS distance
    FROM docs
    ORDER BY distance
    FETCH FIRST 3 ROWS ONLY
"""

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute(sql, {"q": array.array("f", q_vec)})
        print(f"Question: {question}\n")
        for title, content, distance in cur:
            print(f"{distance:.3f}  {title}: {content}")