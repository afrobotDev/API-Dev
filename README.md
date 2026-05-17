# FastAPI + PostgreSQL + Alembic

## 1) Start PostgreSQL (local service)

```bash
sudo systemctl start postgresql
```

## 2) Install dependencies

```bash
uv sync
```

## 3) Create local env file (required)

```bash
cp .env.example .env
```

Edit `.env` and replace placeholders with your real values.

## 4) Run migrations

For a fresh database:

```bash
uv run --env-file .env alembic upgrade head
```

If your database already has the current schema (existing `posts` table from before Alembic):

```bash
uv run --env-file .env alembic stamp head
```

## 5) Run app

```bash
uv run --env-file .env fastapi dev main.py
```

## Common migration commands

Create a new migration (auto-detect model changes):

```bash
uv run --env-file .env alembic revision --autogenerate -m "describe change"
```

Apply latest migrations:

```bash
uv run --env-file .env alembic upgrade head
```

Rollback one revision:

```bash
uv run --env-file .env alembic downgrade -1
```
