from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, field_validator
from database import get_db, init_db

# --- Models ---
class TaskInput(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

    @field_validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v

# --- App ---
app = FastAPI(
    title="Task API",
    description="A simple to-do list API with full CRUD operations",
    version="1.0"
)

init_db()

# --- Root endpoints ---
@app.get("/", summary="API info")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}

# --- Task endpoints ---
@app.get("/tasks", summary="Get all tasks")
def get_tasks(search: str = None, done: bool = None):
    conn = get_db()
    cur = conn.cursor()

    query = "SELECT * FROM tasks"
    params = []
    conditions = []

    if search:
        conditions.append("title LIKE %s")
        params.append(f"%{search}%")

    if done is not None:
        conditions.append("done = %s")
        params.append(int(done))

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return row

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskInput):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
        (task.title, 0)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row

@app.put("/tasks/{task_id}", summary="Update a task")
def update(task_id: int, task_update: TaskUpdate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """UPDATE tasks
           SET title = %s, done = %s, updated_at = CURRENT_TIMESTAMP
           WHERE id = %s RETURNING *""",
        (task_update.title, int(task_update.done), task_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return row

@app.delete("/tasks/{task_id}", summary="Delete a task")
def remove(task_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return Response(status_code=204)