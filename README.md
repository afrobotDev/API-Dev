# FastAPI + PostgreSQL Setup

## 1) Start PostgreSQL

```bash
docker compose up -d
```

## 2) Install dependencies

```bash
uv sync
```

## 3) Set database URL (optional)

Default is already:

`postgresql+psycopg://postgres:postgres@localhost:5432/coolstuff`

If you want to override it:

```bash
cp .env.example .env
```

Run with env file:

```bash
uv run --env-file .env fastapi dev main.py
```

Or run with default env:

```bash
uv run fastapi dev main.py
```

Tables are created automatically at app startup.
