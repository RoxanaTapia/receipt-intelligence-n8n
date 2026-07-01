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
│   └── n8n-claude-standards.md
└── workflows/
    └── hello-world.json      # First exported test workflow
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

## Module 1 deliverables

| Resource | Description |
|----------|-------------|
| [docs/n8n-setup.md](docs/n8n-setup.md) | Docker-based n8n setup and verification |
| [workflows/](workflows/) | Version-controlled n8n workflow exports |
| [docs/n8n-claude-standards.md](docs/n8n-claude-standards.md) | Claude prompting and node naming standards |

## Agent workflow

This repo ships work through Cursor agents — one issue, one branch, one PR. The orchestrator runs `/document` and `/verify` before opening a PR; you approve before push or merge.

**Start here:** [AGENTS.md](AGENTS.md) — agent roster, slash commands (`/ship-issue`, `/verify`, `/document`, `/pedagogical-analysis`), and commit policy.

## Roadmap

High-level modules for the Receipt Intelligence System:

| Module | Focus |
|--------|-------|
| **1 — Foundations** | Agent workflow, Docker n8n, first workflow, Claude standards, README ✅ |
| **2 — Receipt ingestion** | PDF intake and Claude extraction in n8n |
| **3 — Data & categorization** | Structured storage, categories, validation |
| **4 — FastAPI backend** | Supporting APIs where n8n alone is not enough |
| **5 — Query interface** | Natural-language spending and budget questions |
| **6 — Hardening** | Error handling, retries, evaluation |
| **7 — Production readiness** | Deployment, monitoring, operational docs |

Track progress on the [GitHub Project board](https://github.com/users/RoxanaTapia/projects/3).
