from fastapi import FastAPI, HTTPException,Response
from pydantic import BaseModel, validator

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
app = FastAPI()

# ─── In-memory "database" ───────────────────────────────
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book",   "done": False},
    {"id": 3, "title": "Go for a walk", "done": True},
]

# ─── Stage 1 endpoints ──────────────────────────────────
@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

# ─── Stage 2 endpoints ──────────────────────────────────
@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
@app.post("/tasks", status_code=201)
def create_task(task: TaskInput):
    l=len(tasks)
    newtask={"id":l+1,"title":task.title,"done":False}
    tasks.append(newtask)
    return newtask
@app.put("/tasks/{task_id}")
@app.put("/tasks/{task_id}")
def update(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_update.title
            task["done"] = task_update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
@app.delete("/tasks/{task_id}")
def remove(task_id:int):
    for task in tasks:
        if task["id"]==task_id:
            tasks.remove(task)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")