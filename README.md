# Coolstuff — FastAPI + PostgreSQL + JWT Auth

A simple FastAPI-based blog API with PostgreSQL, SQLAlchemy ORM, Alembic migrations, and JWT authentication.

## Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework (w/ Pydantic v2) |
| **PostgreSQL 16** | Database (via Docker Compose or local) |
| **SQLAlchemy 2.0** | ORM (scalars-style queries) |
| **Alembic** | Schema migrations (autogenerate) |
| **Passlib + bcrypt** | Password hashing |
| **python-jose** | JWT encoding/decoding |
| **uv** | Package & project manager |

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/users/` | No | Register a new user |
| POST | `/login` | No | Login, returns JWT |
| GET | `/users/` | JWT | List all users |
| GET | `/users/{id}` | JWT | Get user by ID |
| GET | `/posts/` | JWT | List all posts |
| POST | `/posts/` | JWT | Create a post (owned by you) |
| GET | `/posts/{id}` | JWT | Get post by ID |
| PUT | `/posts/{id}` | JWT | Update your own post |
| DELETE | `/posts/{id}` | JWT | Delete your own post |

## Quick Start

### 1. Start PostgreSQL

```bash
# Option A — use Docker Compose
sudo docker compose up -d

# Option B — use local service
sudo systemctl start postgresql
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` — set `POSTGRES_PASSWORD`, `DATABASE_URL`, and:

```bash
openssl rand -hex 32   # generate a SECRET_KEY for JWT signing
```

### 4. Run migrations

```bash
uv run --env-file .env alembic upgrade head
```

If your database already has the schema (pre-Alembic `posts` table):

```bash
uv run --env-file .env alembic stamp head
```

### 5. Run the app

```bash
uv run --env-file .env fastapi dev main.py
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

## Project Structure

```
├── main.py                  # Re-exports FastAPI app
├── app/
│   ├── main.py              # FastAPI instance & router registration
│   ├── config.py            # SECRET_KEY, ALGORITHM, token expiry
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── db_models.py         # ORM models: Post, User
│   ├── models.py            # Pydantic schemas (request/response)
│   ├── oauth2.py            # JWT creation & get_current_user
│   └── routers/
│       ├── auth.py          # POST /login
│       ├── posts.py         # CRUD /posts
│       └── users.py         # /users endpoints
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/            # Migration revisions
├── pyproject.toml
├── docker-compose.yml       # PostgreSQL 16 container
└── .env.example
```

## Migration Commands

```bash
# Create a migration (auto-detect model changes)
uv run --env-file .env alembic revision --autogenerate -m "describe change"

# Apply latest migrations
uv run --env-file .env alembic upgrade head

# Rollback one revision
uv run --env-file .env alembic downgrade -1
```
