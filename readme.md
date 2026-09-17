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

| Method | Path                 |    Status | Authentication | Description                            |
| ------ | -------------------- | --------: | -------------- | -------------------------------------- |
| GET    | `/protected/profile` | 200 / 401 | Required       | Returns authenticated user information |
| GET    | `/protected/dashb    |           |                |                                        |
