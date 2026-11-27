# Contributing and operating

Notes for people who ship changes to this repo or run it locally. What the workflows do for a reader is on the [README](../README.md).

## Shipping a change

One issue, one branch, one pull request. Roxana reviews and merges. The steps, titles, and tests are in [AGENTS.md](../AGENTS.md).

Track work on the [GitHub Project board](https://github.com/users/RoxanaTapia/projects/3). Linking a pull request moves the issue to In Progress. Merging it moves the issue to Done.

Optional tooling: [GitHub CLI](https://cli.github.com/) (`gh`), [Cursor](https://cursor.com/).

## Module roadmap

| Module | Focus |
|--------|-------|
| **1 — Foundations** | Agent workflow, Docker n8n, first workflow, Claude standards, README ✅ |
| **2 — Receipt ingestion** | PDF intake and Claude extraction in n8n ✅ |
| **3 — Data & categorization** | Structured storage, categories, validation ✅ |
| **4 — Analytics & Q&A** | [`receipt-intelligence-api`](https://github.com/RoxanaTapia/receipt-intelligence-api) — FastAPI analytics and Q&A ✅ |
| **5 — Integration** | n8n ↔ API wiring + [local full-stack runbook](integration.md) ✅ |
| **6 — Reliability** | Claude parse/categorization retries ✅ · Post-persist API HTTP retries ✅ |
| **7 — Delivery** | Live demo / deploy — owned by [`receipt-intelligence-demo`](https://github.com/RoxanaTapia/receipt-intelligence-demo) (API [Dockerfile #25](https://github.com/RoxanaTapia/receipt-intelligence-api/issues/25) supports Compose) |

## Operating locally

Run steps stay in the guides:

| You want to… | Guide |
|--------------|--------|
| Start n8n | [n8n-setup.md](n8n-setup.md) |
| Run n8n and the API together | [integration.md](integration.md) |
| Open the hosted demo | [receipt-intelligence-demo](https://github.com/RoxanaTapia/receipt-intelligence-demo) |
