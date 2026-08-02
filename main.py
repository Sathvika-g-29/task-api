from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, validator
import sqlite3  
# ─── Database setup ─────────────────────────────────────
def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row  # lets you access columns by name like a dict
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done  INTEGER DEFAULT 0
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

# ─── Models ─────────────────────────────────────────────
class TaskInput(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v

# ─── App ────────────────────────────────────────────────
app = FastAPI(
    title="Task API",
    description="A simple to-do list API with full CRUD operations",
    version="1.0"
)

init_db()  # 👈 runs once when server starts


# ─── Stage 1 endpoints ──────────────────────────────────
@app.get("/", summary="API info")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}

# ─── Stage 2 endpoints ──────────────────────────────────
@app.get("/tasks", summary="Get all tasks")
def get_tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(row) for row in rows]
@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return dict(row)
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskInput):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, 0)
    )
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(row)
@app.put("/tasks/{task_id}", summary="Update a task")
def update(task_id: int, task_update: TaskUpdate):
    conn = get_db()
    cursor = conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task_update.title, int(task_update.done), task_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row)
@app.delete("/tasks/{task_id}", summary="Delete a task")
def remove(task_id: int):
    conn = get_db()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return Response(status_code=204)
   