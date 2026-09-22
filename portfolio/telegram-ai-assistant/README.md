# Telegram AI Bot — MVP

A compact Telegram AI assistant built with Python, aiogram, OpenAI API, SQLite conversation memory, environment-based configuration, and Docker.

## Implemented
- Telegram Bot API via aiogram 3
- OpenAI-powered replies
- configurable system prompt
- per-user conversation memory in SQLite
- async message handling
- Docker runtime
- environment-variable configuration

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN='...'
export OPENAI_API_KEY='...'
python app.py
```

## Docker
```bash
docker build -t telegram-ai-bot .
docker run --rm \
  -e TELEGRAM_BOT_TOKEN='...' \
  -e OPENAI_API_KEY='...' \
  telegram-ai-bot
```

## Possible extensions
These are not included in the MVP yet:
- PostgreSQL / Redis
- RAG over documents
- admin roles and dashboard
- payments
- CRM / Google Sheets / webhooks
- voice messages
- analytics and structured logging

This folder is a small work sample intended to show a complete, understandable implementation rather than a feature-heavy demo.
