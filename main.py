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

# ─── Keep your in-memory tasks for now (we'll remove in Stage 1) ───
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book",   "done": False},
    {"id": 3, "title": "Go for a walk", "done": True},
]


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
    return tasks

@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskInput):
    l=len(tasks)
    newtask={"id":l+1,"title":task.title,"done":False}
    tasks.append(newtask)
    return newtask
@app.put("/tasks/{task_id}", summary="Update a task")
def update(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_update.title
            task["done"] = task_update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
@app.delete("/tasks/{task_id}", summary="Delete a task")
def remove(task_id:int):
    for task in tasks:
        if task["id"]==task_id:
            tasks.remove(task)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")