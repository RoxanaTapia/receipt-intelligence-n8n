# Receipt Intelligence System

Turn PDF receipts into structured spending data, then answer natural-language budget questions.

**Stack:** n8n orchestrates PDF ingest, Claude extraction and categorization, and persistence. A sibling [FastAPI](https://github.com/RoxanaTapia/receipt-intelligence-api) service reads the same JSON store for analytics and Q&A.

```text
PDF receipt → extract → categorize → data/receipts/*.json
                                      ↓
                         analytics + natural-language Q&A
```

## Related repositories

| Repo | Role |
|------|------|
| **This repo** (`receipt-intelligence-n8n`) | n8n workflows, categorization, writes `data/receipts/` |
| [`receipt-intelligence-api`](https://github.com/RoxanaTapia/receipt-intelligence-api) | FastAPI analytics and Q&A (reads the shared receipt folder) |

n8n writes categorized JSON to disk; the API reads that folder via `RECEIPT_DATA_PATH`. After persist, the ingest workflow checks coverage, loads an analytics summary, and posts one fixed demo question — it does not POST receipt JSON for ingest. **Demo recipe:** [docs/integration.md](docs/integration.md). **Contract:** [docs/n8n-setup.md](docs/n8n-setup.md#n8n--api-integration-contract).

## Getting started

1. Clone this repo (and the sibling API repo for the full-stack demo).
2. Set up local n8n — [docs/n8n-setup.md](docs/n8n-setup.md) (copy `.env.example` → `.env`, then `docker compose up -d`).
3. Import [workflows/hello-world.json](workflows/hello-world.json) to confirm the editor works.
4. Run the full-stack demo — [docs/integration.md](docs/integration.md).

| Environment | Guide |
|-------------|--------|
| Local n8n | [docs/n8n-setup.md](docs/n8n-setup.md) |
| Local full-stack (n8n + API) | [docs/integration.md](docs/integration.md) |
| Production / cloud | [receipt-intelligence-demo](https://github.com/RoxanaTapia/receipt-intelligence-demo) — Module 7 Delivery |

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Engine + Compose v2). Full-stack demo also needs Python 3.11+ for the API.

## Documentation

Start with the [docs index](docs/README.md) for reading order.

**Pipeline path:** [PDF extraction](docs/pdf-extraction.md) → [categorization](docs/categorization.md) → [data store](data/README.md) → [setup contract](docs/n8n-setup.md#n8n--api-integration-contract) → [integration runbook](docs/integration.md).

| Area | Resource | Description |
|------|----------|-------------|
| Docs index | [docs/README.md](docs/README.md) | Reading order and roles |
| Setup | [docs/n8n-setup.md](docs/n8n-setup.md) | Docker n8n, env vars, n8n ↔ API contract |
| Integration | [docs/integration.md](docs/integration.md) | Local full-stack demo (n8n + API + sample PDF) |
| Extraction | [docs/pdf-extraction.md](docs/pdf-extraction.md) | PDF → Claude → validated JSON |
| Categorization | [docs/categorization.md](docs/categorization.md) | Categories on line items → JSON on disk |
| Schema / prompts / tests | [schema](docs/categorization-schema.md) · [prompts](docs/categorization-prompts.md) · [matrix](docs/categorization-test-matrix.md) | Taxonomy, few-shots, edge cases |
| Standards | [docs/n8n-claude-standards.md](docs/n8n-claude-standards.md) | When to use Claude vs deterministic nodes |
| Data store | [data/README.md](data/README.md) | Filenames, content hash, re-runs |
| Samples | [samples/README.md](samples/README.md) | Anonymized PDF fixtures |
| Workflows | [workflows/](workflows/) | Version-controlled n8n exports |

## Repository structure

```
receipt-intelligence-n8n/
├── AGENTS.md                 # Contributor / Cursor agent workflow
├── .cursor/                  # Agent definitions, commands, and rules
├── docker-compose.yml        # Self-hosted n8n
├── .env.example              # Environment variable template
├── docs/
│   ├── README.md             # Docs index and reading order
│   ├── n8n-setup.md          # Local Docker setup + API contract
│   ├── integration.md        # Full-stack demo runbook
│   ├── n8n-claude-standards.md
│   ├── pdf-extraction.md
│   ├── categorization.md
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

## Roadmap

| Module | Focus |
|--------|-------|
| **1 — Foundations** | Agent workflow, Docker n8n, first workflow, Claude standards, README ✅ |
| **2 — Receipt ingestion** | PDF intake and Claude extraction in n8n ✅ |
| **3 — Data & categorization** | Structured storage, categories, validation ✅ |
| **4 — Analytics & Q&A** | [`receipt-intelligence-api`](https://github.com/RoxanaTapia/receipt-intelligence-api) — FastAPI analytics and Q&A ✅ |
| **5 — Integration** | n8n ↔ API wiring + [local full-stack runbook](docs/integration.md) ✅ |
| **6 — Reliability** | Claude parse/categorization retries ✅ · Post-persist API HTTP retries ✅ |
| **7 — Delivery** | Live demo / deploy — owned by [`receipt-intelligence-demo`](https://github.com/RoxanaTapia/receipt-intelligence-demo) (API [Dockerfile #25](https://github.com/RoxanaTapia/receipt-intelligence-api/issues/25) supports Compose) |

Track progress on the [GitHub Project board](https://github.com/users/RoxanaTapia/projects/3).

## Contributor notes

This repo ships work through Cursor agents — one issue, one branch, one PR. See [AGENTS.md](AGENTS.md) for the agent roster, slash commands (`/ship-issue`, `/verify`, `/document`, `/lecture-on-issue`), and commit policy.

Optional tooling for contributors: [GitHub CLI](https://cli.github.com/) (`gh`), [Cursor](https://cursor.com/).
