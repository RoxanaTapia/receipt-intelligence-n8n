# Receipt Intelligence System

Process PDF receipts, extract and categorize spending with Claude, and answer natural-language budget questions — orchestrated in **n8n**, with **FastAPI** as a supporting backend when custom logic is needed.

## Related repositories

| Repo | Role |
|------|------|
| **This repo** (`receipt-intelligence-n8n`) | n8n workflows, categorization, `data/receipts/` JSON output |
| [`receipt-intelligence-api`](https://github.com/RoxanaTapia/receipt-intelligence-api) | FastAPI analytics and Q&A (Module 4 — open in Cursor for API `/ship-issue`) |

**Integration (local):** n8n writes receipt JSON to disk; the API reads the same folder via `RECEIPT_DATA_PATH`. After persist, the ingest workflow smokes coverage (`GET /health`, `GET /analytics/receipts`) then calls `GET /analytics/summary?preset=last_month` via `API_BASE_URL` — it does not POST receipt JSON. See [docs/n8n-setup.md](docs/n8n-setup.md#n8n--api-integration-contract).

## Repository structure

```
receipt-intelligence-n8n/
├── AGENTS.md                 # Cursor agent workflow (start here for shipping)
├── .cursor/                  # Agent definitions, commands, and rules
├── docker-compose.yml        # Self-hosted n8n
├── .env.example              # Environment variable template
├── docs/
│   ├── n8n-setup.md          # Local Docker setup
│   ├── n8n-claude-standards.md
│   ├── pdf-extraction.md     # PDF extraction pipeline guide
│   ├── categorization.md     # Categorization pipeline guide
│   ├── categorization-schema.md
│   ├── categorization-prompts.md
│   └── categorization-test-matrix.md
├── samples/
│   ├── README.md             # Anonymized PDF catalog and privacy rules
│   └── receipts/             # Committed public-safe PDF fixtures
├── data/
│   ├── README.md             # Receipt JSON store contract
│   └── receipts/             # Categorized JSON output (runtime)
└── workflows/
    ├── hello-world.json
    └── receipt-pdf-ingest.json
```

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose v2)
- [GitHub CLI](https://cli.github.com/) (`gh`) — issues and PRs
- [Cursor](https://cursor.com/) — agent-assisted development

## Getting started

1. **Clone this repo** and open it in Cursor.
2. **Set up local n8n** — follow [docs/n8n-setup.md](docs/n8n-setup.md) (copy `.env.example` → `.env`, then `docker compose up -d`).
3. **Import a workflow** — open the n8n UI and import [workflows/hello-world.json](workflows/hello-world.json).
4. **Ship work via agents** — pick an issue on the [Project board](https://github.com/users/RoxanaTapia/projects/3), then run `/ship-issue #NN` (see [AGENTS.md](AGENTS.md)).

### Deployment

| Environment | Where to look |
|-------------|---------------|
| **Local development** | [docs/n8n-setup.md](docs/n8n-setup.md) |
| **Production / cloud** | Not documented yet — a future milestone will add a dedicated deployment guide |

## Documentation

| Area | Resource | Description |
|------|----------|-------------|
| Setup | [docs/n8n-setup.md](docs/n8n-setup.md) | Docker-based n8n setup, env vars, n8n ↔ API config contract |
| Workflows | [workflows/](workflows/) | Version-controlled n8n workflow exports |
| Standards | [docs/n8n-claude-standards.md](docs/n8n-claude-standards.md) | Claude prompting and node naming standards |
| Extraction | [docs/pdf-extraction.md](docs/pdf-extraction.md) | PDF → Claude → validated JSON pipeline |
| Pipeline | [docs/categorization.md](docs/categorization.md) | Categorization pipeline — validated categories on disk |
| Schema | [docs/categorization-schema.md](docs/categorization-schema.md) | Spending category taxonomy and output schema |
| Prompts | [docs/categorization-prompts.md](docs/categorization-prompts.md) | Categorization prompt with few-shot examples |
| Test matrix | [docs/categorization-test-matrix.md](docs/categorization-test-matrix.md) | Edge-case categorization verification |
| Data store | [data/README.md](data/README.md) | Receipt JSON filenames, hash, re-runs |
| Samples | [samples/README.md](samples/README.md) | Anonymized PDF fixtures and privacy rules |

## Agent workflow

This repo ships work through Cursor agents — one issue, one branch, one PR. The orchestrator runs `/document` and `/verify` before opening a PR; you approve before push or merge.

**Start here:** [AGENTS.md](AGENTS.md) — agent roster, slash commands (`/ship-issue`, `/verify`, `/document`, `/lecture-on-issue`), and commit policy.

## Roadmap

High-level modules for the Receipt Intelligence System:

| Module | Focus |
|--------|-------|
| **1 — Foundations** | Agent workflow, Docker n8n, first workflow, Claude standards, README ✅ |
| **2 — Receipt ingestion** | PDF intake and Claude extraction in n8n ✅ |
| **3 — Data & categorization** | Structured storage, categories, validation ✅ |
| **4 — Analytics & Q&A** | [`receipt-intelligence-api`](https://github.com/RoxanaTapia/receipt-intelligence-api) — FastAPI backend, spending analytics, natural-language questions ✅ |
| **5 — Integration** | In progress — post-persist coverage smoke + analytics summary; Q&A HTTP and runbook in follow-ups |
| **6 — Reliability** | Planned — Claude parse/categorization retries and workflow hardening |
| **7 — Delivery** | Planned — live demo / production readiness, deployment and operational docs |

Track progress on the [GitHub Project board](https://github.com/users/RoxanaTapia/projects/3).
