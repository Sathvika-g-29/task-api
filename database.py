import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tasks.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)  # 👈 uses absolute path now
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            done       INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        conn.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", [
            ("Buy groceries", 0),
            ("Read a book",   0),
            ("Go for a walk", 1),
        ])
    conn.commit()
    conn.close()