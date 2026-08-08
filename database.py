import psycopg
import psycopg.rows
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    conn = psycopg.connect(DATABASE_URL, row_factory=psycopg.rows.dict_row)
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id         SERIAL PRIMARY KEY,
            title      TEXT NOT NULL,
            done       INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()["count"]
    if count == 0:
        cur.executemany("INSERT INTO tasks (title, done) VALUES (%s, %s)", [
            ("Buy groceries", 0),
            ("Read a book",   0),
            ("Go for a walk", 1),
        ])
    conn.commit()
    cur.close()
    conn.close()