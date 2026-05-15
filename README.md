# FastAPI + PostgreSQL Setup

## 1) Start PostgreSQL (local service)

```bash
sudo systemctl start postgresql
```

## 2) Install dependencies

```bash
uv sync
```

## 3) Create local env file (required)

cp .env.example .env

Edit `.env` and replace `<CHANGE_ME>` with your real Postgres password.

## 4) Run app with env file

```bash
uv run --env-file .env fastapi dev main.py
```

Tables are created automatically at app startup.
