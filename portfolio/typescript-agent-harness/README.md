# TypeScript Agent Tool-Loop Harness

A small, dependency-light work sample showing how to structure an LLM-style agent loop without hiding the control flow inside a framework.

## What it demonstrates

- explicit tool allowlisting
- bounded agent loops (`maxSteps`)
- structured tool success/error messages
- validation before business actions
- failures returned to the model instead of crashing the process
- human-approval state for a construction material request
- deterministic tests with a scripted model adapter

The included construction tool validates a material request and returns `needs-human-approval`. A production WhatsApp agent could swap the scripted model adapter for OpenAI/Anthropic and connect approved requests to a database, ERP, or messaging workflow.

## Verification

The sample was compiled with TypeScript 5.8.3 and its four deterministic tests passed before publishing.

## Run tests

```bash
tsc -p tsconfig.json
node dist/test/run-tests.js
```

## Deliberate scope

This is a work sample, not a hosted production service. It does not claim WhatsApp/Meta integration, persistence, authentication, or production monitoring.
