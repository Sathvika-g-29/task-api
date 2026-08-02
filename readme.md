# Task API — W3·A1

A simple CRUD REST API built with FastAPI and SQLite. Tasks are stored in a real database and survive server restarts.

---

## What changed from Assignment 1

In Assignment 1, tasks were stored in a Python list in memory — every restart wiped the data.

This version replaces that list with a SQLite database. The API endpoints are **identical**. The client never notices the difference. Only the storage layer changed.

---

## Why SQLite?

- No separate server to install or run
- Stored as a single file (`tasks.db`) sitting right next to the code
- Built into Python — no pip install needed
- Perfect for learning and small projects

For production apps you'd swap SQLite for PostgreSQL or MySQL, but the SQL queries would look almost the same.

---

## Project structure

```
project/
├── main.py       # FastAPI app + all routes
├── tasks.db      # SQLite database file (auto-created on first run)
├── .gitignore    # excludes tasks.db from version control
└── README.md
```

---

## How to run

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

**2. Install dependencies**
```bash
pip install fastapi uvicorn
```

**3. Start the server**
```bash
uvicorn main:app --reload
```

The database file `tasks.db` is created automatically on first run.
Three example tasks are inserted only once — they won't duplicate on restarts.

**4. Open the API docs**
```
http://127.0.0.1:8000/docs
```

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a single task |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/health` | Health check |

---

## Database

- **File:** `tasks.db` (created automatically)
- **Table:** `tasks`
- **Columns:** `id` (integer, primary key), `title` (text), `done` (integer 0/1)

The table is created on startup if it doesn't exist:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done  INTEGER DEFAULT 0
);
```

---

## Example SQL queries

Here are some queries explored manually during development:

```sql
-- List every task
SELECT * FROM tasks;

-- Show only completed tasks
SELECT * FROM tasks WHERE done = 1;

-- Count all tasks
SELECT COUNT(*) FROM tasks;

-- Mark every task as completed
UPDATE tasks SET done = 1;

-- Delete all completed tasks
DELETE FROM tasks WHERE done = 1;
```

---

## Shell output screenshot

![SQLite shell output](screenshot.png)

> Querying the database directly from the Python shell to verify rows are stored correctly.

---

## Key idea

> APIs describe **what** your application does. Databases describe **where** your application stores its data.

The client sends the same requests to the same endpoints. Only the implementation behind those endpoints changed.