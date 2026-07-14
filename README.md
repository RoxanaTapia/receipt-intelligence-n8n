# Receipt Intelligence System

Process PDF receipts, extract and categorize spending with Claude, and answer natural-language budget questions — orchestrated in **n8n**, with **FastAPI** as a supporting backend when custom logic is needed.

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
│   ├── pdf-extraction.md     # Module 2 pipeline guide
│   ├── categorization.md     # Module 3 pipeline guide
│   ├── categorization-schema.md
│   └── categorization-prompts.md
├── samples/receipts/         # Anonymized PDF fixtures
├── data/receipts/            # Categorized JSON output
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

## Module deliverables

| Module | Resource | Description |
|--------|----------|-------------|
| 1 | [docs/n8n-setup.md](docs/n8n-setup.md) | Docker-based n8n setup and verification |
| 1 | [workflows/](workflows/) | Version-controlled n8n workflow exports |
| 1 | [docs/n8n-claude-standards.md](docs/n8n-claude-standards.md) | Claude prompting and node naming standards |
| 2 | [docs/pdf-extraction.md](docs/pdf-extraction.md) | PDF → Claude → validated JSON pipeline |
| 3 | [docs/categorization.md](docs/categorization.md) | Categorization pipeline — validated categories on disk |
| 3 | [docs/categorization-schema.md](docs/categorization-schema.md) | Spending category taxonomy and output schema |
| 3 | [docs/categorization-prompts.md](docs/categorization-prompts.md) | Categorization prompt with few-shot examples |
| 3 | [docs/categorization-test-matrix.md](docs/categorization-test-matrix.md) | Edge-case categorization verification |

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
| **4 — FastAPI backend** | Supporting APIs where n8n alone is not enough |
| **5 — Query interface** | Natural-language spending and budget questions |
| **6 — Hardening** | Error handling, retries, evaluation |
| **7 — Production readiness** | Deployment, monitoring, operational docs |

Track progress on the [GitHub Project board](https://github.com/users/RoxanaTapia/projects/3).
