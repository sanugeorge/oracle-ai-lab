import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return oracledb.connect(
        user=os.getenv("ORA_USER"),
        password=os.getenv("ORA_PASSWORD"),
        dsn=os.getenv("ORA_DSN"),
    )

def main():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT banner FROM v$version FETCH FIRST 1 ROW ONLY")
                print("Connected to:", cur.fetchone()[0])

                cur.execute("SELECT id, title, body FROM notes ORDER BY id")
                for row in cur:
                    print(row)
    except oracledb.Error as e:
        print("Oracle error:", e)

if __name__ == "__main__":
    main()