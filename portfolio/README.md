# Work Samples

Small, inspectable projects used as practical work samples.

## Fixed-scope starter offers

These are intentionally small first milestones so a buyer can verify the result before committing to a larger project.

| Deliverable | Starter price | Typical first milestone |
| --- | ---: | --- |
| CSV / Excel cleanup or transformation | $20 | Clean, normalize, deduplicate, and export a reproducible result |
| API / webhook integration diagnostic + fix | $25 | Reproduce the issue, implement one bounded integration/fix, document handoff |
| Lead capture + webhook backend | $35 | FastAPI endpoint, validation, persistence, webhook notification, Docker |
| Telegram bot adaptation | $40 | Adapt the existing Python bot base to one clearly scoped workflow |
| Lead triage / routing automation | $25 | Deterministic scoring/normalization and JSON output for CRM/n8n/Make |
| Small AI/API automation prototype | $50 | One working end-to-end automation with explicit inputs/outputs and setup notes |

Prices are starter milestones, not promises for unlimited scope. Credentials, hosting costs, paid APIs, and production hardening are quoted separately. No access keys or secrets belong in source code.

## 1. TypeScript Agent Tool-Loop Harness
**TypeScript · Agent loops · Tool allowlisting · Validation · Deterministic tests**

A framework-light agent harness with bounded steps, explicit tool allowlisting, structured tool success/error messages, and a human-approval state for business actions.

[Open the project](./typescript-agent-harness)

### Demonstrates
- visible, auditable agent control flow
- fail-closed max-step guard
- safe handling of unknown tools
- validation before business actions
- deterministic scripted-model tests (4/4 passed before publishing)

## 2. Telegram AI Assistant
**Python · aiogram · OpenAI API · SQLite · Docker**

A compact end-to-end Telegram AI assistant with per-user conversation memory and environment-based configuration.

[Open the project](./telegram-ai-assistant)

### Demonstrates
- Python async application structure
- third-party AI API integration
- persistent state with SQLite
- configuration/secrets separated from code
- deployable Docker packaging

## 3. Lead Capture Automation
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

## 4. Lead Triage Automation
**Python · JSON CLI · Deterministic scoring · Tests**

A dependency-free automation that validates and normalizes inbound leads, scores them using explicit business rules, assigns hot/warm/cold priority, and emits machine-readable JSON for a CRM, webhook, n8n, Make, or another service.

[Open the project](./lead-triage-automation)

### Demonstrates
- deterministic business rules
- validation and normalization
- CLI/stdin workflows
- machine-readable output
- automation without unnecessary LLM dependence

All samples are deliberately small enough to inspect quickly and explicit about what is implemented versus what would be added for production.
