import os
import array
from pathlib import Path
import ollama
import oracledb
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DOCS = [
    ("Indexes", "An index is a database structure that speeds up data retrieval by avoiding full table scans."),
    ("Execution plans", "An execution plan shows how Oracle will run a SQL statement, including join methods and access paths."),
    ("AWR reports", "Automatic Workload Repository reports summarise database performance over a time period."),
    ("Backups", "RMAN is Oracle's tool for backing up and restoring databases."),
    ("Python lists", "A Python list is an ordered, changeable collection of items written in square brackets."),
    ("Python dictionaries", "A dictionary stores key and value pairs and lets you look up values by key."),
    ("Docker containers", "A container packages an application with its dependencies so it runs the same everywhere."),
    ("Vector search", "Vector search finds items whose embeddings are closest in meaning to a query."),
]

def get_connection():
    return oracledb.connect(
        user=os.getenv("ORA_USER"),
        password=os.getenv("ORA_PASSWORD"),
        dsn=os.getenv("ORA_DSN"),
    )

texts = [f"{title}: {content}" for title, content in DOCS]
embeddings = ollama.embed(model="embeddinggemma", input=texts)["embeddings"]

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM docs")  # so re-running doesn't create duplicates
        for (title, content), vec in zip(DOCS, embeddings):
            cur.execute(
                "INSERT INTO docs (title, content, embedding) VALUES (:t, :c, :e)",
                {"t": title, "c": content, "e": array.array("f", vec)},
            )
    conn.commit()
    print(f"Loaded {len(DOCS)} documents.")