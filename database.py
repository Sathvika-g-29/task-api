import sqlite3

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done  INTEGER DEFAULT 0
        )
    """)

    # Insert 3 example tasks ONLY if table is empty
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        conn.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", [
            ("Buy groceries", 0),
            ("Walk the dog", 0),
            ("Read a book", 1),
        ])

    conn.commit()
    conn.close()

# Call this when the app starts
init_db()