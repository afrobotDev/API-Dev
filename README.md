# Coolstuff API

A production-ready FastAPI blog API with PostgreSQL, JWT authentication, SQLAlchemy models, Alembic migrations, and vote tracking.

Coolstuff exposes a small social posting backend: users can register, log in, create posts, search and paginate posts, update or delete their own posts, and upvote or remove votes from posts.

## Features

- Email/password user registration with bcrypt hashing
- OAuth2 password login that returns a bearer JWT
- Protected user, post, and vote routes
- Post ownership checks for updates and deletes
- Post search across title and content
- Pagination with `limit` and `offset`
- Vote counts included in post responses
- Alembic-managed PostgreSQL schema
- Docker Compose setup for local app + database
- Render deployment blueprint

## Tech Stack

| Layer | Tooling |
| --- | --- |
| API | FastAPI, Pydantic v2 |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Auth | OAuth2 password flow, JWT, python-jose |
| Passwords | passlib, bcrypt |
| Package manager | uv |
| Deployment | Docker, Docker Compose, Render |

## Project Structure

```text
.
├── app/
│   ├── main.py              # FastAPI app, CORS, router registration
│   ├── config.py            # JWT settings loaded from environment
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── db_models.py         # SQLAlchemy tables: users, posts, votes
│   ├── models.py            # Pydantic request/response schemas
│   ├── oauth2.py            # JWT creation and current-user dependency
│   ├── security.py          # Password hashing context
│   └── routers/
│       ├── auth.py          # POST /login
│       ├── users.py         # User registration and lookup
│       ├── posts.py         # Post CRUD, search, pagination
│       └── votes.py         # Vote and unvote endpoint
├── alembic/
│   ├── env.py
│   └── versions/            # Database migration history
├── main.py                  # ASGI entrypoint that exports app.main:app
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python 3.13+
- `uv`
- PostgreSQL, or Docker with Docker Compose

Install `uv` if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Environment Variables

Create a local environment file:

```bash
cp .env.example .env
```

Expected variables:

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | Yes | SQLAlchemy database URL |
| `SECRET_KEY` | Yes | Secret used to sign JWTs |
| `POSTGRES_PASSWORD` | Yes for Docker Compose | Password for the local Postgres container |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | JWT lifetime in minutes. Defaults to `30` |

Generate a strong JWT secret:

```bash
openssl rand -hex 32
```

For local Docker Compose, use port `5433` from the host because the Compose file maps PostgreSQL as `127.0.0.1:5433->5432`:

```env
POSTGRES_PASSWORD=change-me
DATABASE_URL=postgresql+psycopg://postgres:change-me@localhost:5433/coolstuff
SECRET_KEY=replace-with-openssl-output
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Quick Start

### Option 1: Run Everything With Docker Compose

```bash
docker compose up --build
```

The API will be available at:

- API: `http://localhost:8001`
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

The container command runs migrations automatically before starting the API.

### Option 2: Run the API Locally

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Install dependencies:

```bash
uv sync
```

Apply migrations:

```bash
uv run --env-file .env alembic upgrade head
```

Start the development server:

```bash
uv run --env-file .env fastapi dev main.py
```

The API will be available at `http://localhost:8000`.

## API Reference

### Authentication

Most routes require a bearer token:

```http
Authorization: Bearer <access_token>
```

Login uses FastAPI's OAuth2 password form. Send the user's email as `username`.

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/users/` | No | Register a user |
| `POST` | `/login` | No | Log in and receive a JWT |

### Users

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/users/` | Yes | List all users |
| `GET` | `/users/{id}` | Yes | Get one user by ID |

### Posts

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/posts/` | Yes | List posts with vote counts |
| `POST` | `/posts/` | Yes | Create a post owned by the current user |
| `GET` | `/posts/{id}` | Yes | Get one post with its vote count |
| `PUT` | `/posts/{id}` | Yes | Update one of your own posts |
| `DELETE` | `/posts/{id}` | Yes | Delete one of your own posts |

`GET /posts/` supports query parameters:

| Parameter | Default | Description |
| --- | --- | --- |
| `limit` | `10` | Number of posts to return. Must be between `1` and `100` |
| `offset` | `0` | Number of posts to skip |
| `search` | none | Case-insensitive search across title and content |

Example:

```http
GET /posts/?limit=20&offset=0&search=fastapi
```

### Votes

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/vote/` | Yes | Add or remove the current user's vote for a post |

Request body:

```json
{
  "post_id": 1,
  "vote_dir": 1
}
```

Use `vote_dir: 1` to add a vote and `vote_dir: 0` to remove it.

## Example Workflow

Register a user:

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"ada@example.com","password":"secret123"}'
```

Log in:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ada@example.com&password=secret123" \
  | python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
```

Create a post:

```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello FastAPI","content":"First post","published":true,"description":"Intro post"}'
```

Vote for a post:

```bash
curl -X POST http://localhost:8000/vote/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"post_id":1,"vote_dir":1}'
```

## Database Migrations

Apply all migrations:

```bash
uv run --env-file .env alembic upgrade head
```

Create a new autogenerated migration after changing SQLAlchemy models:

```bash
uv run --env-file .env alembic revision --autogenerate -m "describe change"
```

Roll back one migration:

```bash
uv run --env-file .env alembic downgrade -1
```

If you connect to a database that already has the expected schema and only needs Alembic version tracking:

```bash
uv run --env-file .env alembic stamp head
```

## Docker

Build the API image:

```bash
docker build -t coolstuff-api .
```

Run the full local stack:

```bash
docker compose up --build
```

Stop the stack:

```bash
docker compose down
```

Remove the local database volume:

```bash
docker compose down -v
```

## Deployment

This repository includes `render.yaml` for Render Blueprint deployment. It defines:

- A Docker web service named `coolstuff-api`
- A managed PostgreSQL database named `coolstuff-db`
- Runtime environment variables for `DATABASE_URL`, `SECRET_KEY`, and `ACCESS_TOKEN_EXPIRE_MINUTES`

The Docker start command applies Alembic migrations before launching FastAPI:

```bash
uv run alembic upgrade head && uv run fastapi run main.py --port 8000
```

## Development Notes

- `main.py` at the repository root is the ASGI entrypoint used by FastAPI and Docker.
- `app/main.py` registers all routers and enables permissive CORS.
- `DATABASE_URL` and `SECRET_KEY` are required at import time, so run commands with `--env-file .env` or export the variables in your shell.
- Passwords must be at least 6 characters and no more than 72 UTF-8 bytes because bcrypt truncates longer inputs.
- Post update and delete operations are restricted to the user who owns the post.
