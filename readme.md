# Task API — FastAPI + PostgreSQL + Supabase Authentication

A containerized FastAPI Task API with PostgreSQL storage and Supabase Authentication.

The project provides:

* Task CRUD operations
* User signup and login
* JWT-based authentication
* Protected API endpoints
* Public API endpoint
* Protected logout
* Swagger UI with Bearer token authentication

## Tech Stack

* **FastAPI** — REST API framework
* **PostgreSQL** — Database
* **Docker / Docker Compose** — Containerization
* **Supabase Auth** — User authentication and JWT management
* **Pydantic** — Request validation
* **HTTPBearer** — Bearer token authentication in FastAPI

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Sathvika-g-29/task-api.git
cd task-api
```

### 2. Create the environment file

Copy `.env.example` to `.env` and add your local configuration:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

**Never commit `.env` or expose Supabase credentials.**

### 3. Start the application

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Authentication Flow

The application uses Supabase as the identity provider.

```text
User
  ↓
FastAPI /auth/signup
  ↓
Supabase Auth
  ↓
User account created

User
  ↓
FastAPI /auth/login
  ↓
Supabase Auth
  ↓
Access Token + Refresh Token
  ↓
Protected FastAPI endpoints
  ↓
Supabase verifies the access token
```

The backend uses a reusable authentication dependency to protect routes that require a valid Bearer token.

## API Endpoints

### Authentication

| Method | Path           | Status | Authentication | Description                             |
| ------ | -------------- | -----: | -------------- | --------------------------------------- |
| POST   | `/auth/signup` |    201 | Public         | Create a new user                       |
| POST   | `/auth/login`  |    200 | Public         | Login and receive access/refresh tokens |
| POST   | `/auth/logout` |    204 | Required       | Logout the authenticated user           |

### Public

| Method | Path           | Status | Authentication | Description                |
| ------ | -------------- | -----: | -------------- | -------------------------- |
| GET    | `/public/info` |    200 | Public         | Returns public information |

### Protected

| Method | Path                   |    Status | Authentication | Description                            |
| ------ | ---------------------- | --------: | -------------- | -------------------------------------- |
| GET    | `/protected/profile`   | 200 / 401 | Required       | Returns authenticated user information |
| GET    | `/protected/dashboard` | 200 / 401 | Required       | Example protected dashboard            |

### Tasks

| Method | Path          |    Status | Description   |
| ------ | ------------- | --------: | ------------- |
| GET    | `/tasks`      |       200 | Get all tasks |
| GET    | `/tasks/{id}` | 200 / 404 | Get one task  |
| POST   | `/tasks`      | 201 / 400 | Create a task |
| PUT    | `/tasks/{id}` | 200 / 404 | Update a task |
| DELETE | `/tasks/{id}` | 204 / 404 | Delete a task |

## Using Protected Endpoints

1. Create an account using `/auth/signup`.
2. Login using `/auth/login`.
3. Copy the returned `access_token`.
4. Open `/docs`.
5. Click **Authorize**.
6. Enter the access token in the HTTPBearer field.
7. Execute a protected endpoint such as `/protected/profile`.

Protected endpoints reject requests when the access token is missing, malformed, invalid, or expired.

## Example Login Response

```json
{
  "access_token": "your-access-token",
  "refresh_token": "your-refresh-token"
}
```

Do not publish real tokens.

## Project Structure

```text
task-api/
├── main.py
├── database.py
├── supabase_client.py
├── auth_dependency.py
├── routers/
│   ├── __init__.py
│   └── auth.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Important Files

* `main.py` — FastAPI application, task routes, public and protected routes
* `database.py` — PostgreSQL connection and task table initialization
* `supabase_client.py` — Supabase client configuration
* `auth_dependency.py` — Reusable Bearer token verification dependency
* `routers/auth.py` — Signup, login, and logout endpoints
* `docker-compose.yml` — API and PostgreSQL services
* `.env.example` — Environment variable template
* `.env` — Local secrets; ignored by Git

## PostgreSQL Persistence

PostgreSQL runs as a Docker service and uses a named volume for persistent data.

This means task data remains available after stopping and restarting the containers.

## Swagger

FastAPI's Swagger UI is available at:

```text
http://localhost:8000/docs
```

The protected endpoints use HTTP Bearer authentication, allowing the access token to be supplied through Swagger's **Authorize** button.

## Security Notes

* Supabase credentials are stored in environment variables.
* `.env` is excluded from Git.
* Access tokens should never be committed to the repository.
* Protected routes use a reusable authentication dependency.
* The backend verifies authentication through Supabase rather than hardcoding users or tokens.
