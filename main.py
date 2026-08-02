from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, validator
from database import get_db, init_db  

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

init_db()  # now calls the correct one from database.py

# ─── Root endpoints ──────────────────────────────────────
@app.get("/", summary="API info")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}

# ─── Task endpoints ──────────────────────────────────────
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
        """UPDATE tasks 
           SET title = ?, done = ?, updated_at = CURRENT_TIMESTAMP 
           WHERE id = ?""",
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