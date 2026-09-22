# Lead Capture Automation

A small business-automation work sample: receive leads through an HTTP API, validate them, store them in SQLite, deduplicate retry submissions, and optionally notify a webhook.

## What it demonstrates

- FastAPI + Pydantic input validation
- SQLite persistence
- idempotent duplicate handling
- webhook integration with failure isolation
- environment-based configuration
- Docker packaging
- deterministic unit tests

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` for the generated API UI.

## Tests

```bash
python -m unittest discover -s tests -v
```

The work sample was locally syntax-checked and its three unit tests passed before publishing.

## Deliberate scope

This is a compact work sample, not a hosted production service. Production extensions could include PostgreSQL, auth/RBAC, retries/queueing, Google Sheets or CRM sync, email delivery, structured logging, metrics, and a deployment pipeline.
