# Work Samples

Small, inspectable projects used as practical work samples.

## 1. Telegram AI Assistant
**Python · aiogram · OpenAI API · SQLite · Docker**

A compact end-to-end Telegram AI assistant with per-user conversation memory and environment-based configuration.

[Open the project](./telegram-ai-assistant)

### Demonstrates
- Python async application structure
- third-party AI API integration
- persistent state with SQLite
- configuration/secrets separated from code
- deployable Docker packaging

## 2. Lead Capture Automation
**Python · FastAPI · Pydantic · SQLite · Webhooks · Docker**

A small business automation that accepts and validates incoming leads, stores them, prevents duplicate retry submissions, and can notify an external webhook without losing the lead if notification fails.

[Open the project](./lead-capture-automation)

### Demonstrates
- REST API design with FastAPI
- business input validation
- SQLite persistence
- idempotent duplicate handling
- webhook integration and failure isolation
- unit tests (3/3 passed before publishing)
- Docker packaging

Both samples are deliberately small enough to inspect quickly and explicit about what is implemented versus what would be added for production.
