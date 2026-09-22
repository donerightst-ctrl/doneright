# Lead Triage Automation — Python Work Sample

Small, dependency-free automation that turns raw inbound leads into a prioritized queue.

It demonstrates practical backend/automation work: validation, normalization, deterministic scoring, JSON input/output, CLI usage, and tests. No external service or API key is required.

## What it does

- accepts JSON leads from a file or stdin
- validates required fields
- normalizes email/company/source data
- scores leads using explicit business rules
- assigns `hot`, `warm`, or `cold`
- sorts the output so the most actionable leads come first
- emits machine-readable JSON suitable for a CRM, webhook, n8n, Make, or another Python service

## Run

```bash
python lead_triage.py sample_leads.json
python -m unittest test_lead_triage.py -v
```

The rules are intentionally transparent rather than hidden behind an LLM. In a production workflow, an LLM enrichment step can be added after deterministic validation/scoring, where it provides value without making the core pipeline unpredictable.
