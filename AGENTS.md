# AGENTS.md — Receipt Intelligence n8n

How we use Cursor agents, rules, and commands in this repository.

## Project Vision

Build a clean, production-style system that processes PDF receipts, extracts and categorizes data using Claude, and answers natural language questions about spending and budget.

**Stack:** n8n (core) · Claude · FastAPI (supporting backend)

This repo **writes** categorized receipts to `data/receipts/`. Sibling [receipt-intelligence-api](https://github.com/RoxanaTapia/receipt-intelligence-api) **reads** them via `RECEIPT_DATA_PATH`.

## Project references

Agents use generic language; this table maps terms to **this repo**. Other projects: update here only — keep `.cursor/agents/` unchanged.

| Term | Path |
|------|------|
| Prompt / Claude standards | [`docs/n8n-claude-standards.md`](docs/n8n-claude-standards.md) |
| Categorization pipeline | [`docs/categorization.md`](docs/categorization.md) |
| Categorization schema | [`docs/categorization-schema.md`](docs/categorization-schema.md) |
| Categorization prompts | [`docs/categorization-prompts.md`](docs/categorization-prompts.md) |
| Categorization test matrix | [`docs/categorization-test-matrix.md`](docs/categorization-test-matrix.md) |
| Receipt data store | [`data/README.md`](data/README.md) |
| Sample receipt JSON | [`data/receipts/example.json`](data/receipts/example.json) |
| Workflow exports | [`workflows/receipt-pdf-ingest.json`](workflows/receipt-pdf-ingest.json) |
| Setup guide | [`docs/n8n-setup.md`](docs/n8n-setup.md) |
| PDF pipeline guide | [`docs/pdf-extraction.md`](docs/pdf-extraction.md) |
| Sample PDFs (anonymized) | [`samples/receipts/`](samples/receipts/) |
| Sample originals (gitignored) | `samples/receipts/originals/` — see [`samples/README.md`](samples/README.md) |

## Current Focus

- **This repo:** Modules 1–3 complete; **Module 5 — Integration** in progress (n8n ↔ API wiring)
- **Next:** Module 6 — Reliability (Claude retries); Module 7 — Delivery (live demo / deploy)
- **Sibling:** [receipt-intelligence-api](https://github.com/RoxanaTapia/receipt-intelligence-api) — Module 4 analytics + Q&A complete; open that repo for API `/ship-issue`
- **Recent docs:** Module 4 handoff and Q&A routing pointers in Claude standards

## Core Principles

- Keep things simple, readable, and maintainable
- Small, focused functions and changes
- One issue → one branch → one PR
- Prioritize clarity and long-term quality

## Agent Roster

| Role | Responsibility | Notes |
|------|----------------|-------|
| `milestone-orchestrator` | Coordinates shipping, branches, commits | Only agent allowed to commit; decides when to call specialists |
| `docs-writer` | Documentation draft and review | `/document`; ownership/handoff in agent, style in `documentation.mdc` |
| `verifier` | Quality checks and acceptance criteria before PR | `/verify`; blocks PR if criteria ❌ missing |
| `software-engineering-professor` | Teaches issues and concepts | `/lecture-on-issue`; does not ship |
| `n8n-engineer` | n8n workflows and integration | Workflow structure and nodes; see **Project references** |
| `claude-prompt-engineer` | Claude prompts in n8n | Prompt standards doc in **Project references** |

## Workflow

1. Pick a GitHub issue on the Project board.
2. *(Optional)* `/lecture-on-issue #NN` — learn before building.
3. `/ship-issue #NN` — orchestrator implements with specialist support.
4. Inside shipping: run **`/document`** only if the issue creates or updates documentation (orchestrator decides per triggers in `milestone-orchestrator.md`); otherwise skip and note in the PR → always run **`/verify`** (maps acceptance criteria) → PR with test plan from the same criteria.
5. Human reviews PR test plan and approves before push or merge.
6. After merge: **`/ship-complete #NN`** — tick acceptance criteria checkboxes on the issue.

Project **Status** uses GitHub Project automations (PR linked → In Progress; merged → Done).

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/ship-issue` | Ship one GitHub issue end-to-end |
| `/document` | Run docs-writer review (ownership, handoff, style) |
| `/verify` | Quality verification and acceptance criteria coverage before PR |
| `/ship-complete` | After merge — tick issue acceptance criteria checkboxes |
| `/lecture-on-issue` | Teach an issue (learner mode) |

## Rules

| Rule | Scope |
|------|-------|
| `.cursor/rules/documentation.mdc` | Markdown doc style |
| `.cursor/rules/elegant-minimal-python.mdc` | Python code style |

**When to call specialists:** `.cursor/agents/milestone-orchestrator.md` (shipping pipeline and triggers)

**Documentation process** (ownership, handoff): `.cursor/agents/docs-writer.md`

**Inline vs repo docs:** Docstrings and code comments are part of normal implement work (`elegant-minimal-python.mdc`). Repo markdown goes through docs-writer (`/document`) when the orchestrator's triggers match.

**Documentation accuracy:** When doc issues describe workflows or AI behavior, the orchestrator consults specialists before `/document` — see `milestone-orchestrator.md`.

## Commit & PR Policy

- Granular, reviewable commits (ideally 1–4 per issue)
- Only `milestone-orchestrator` creates commits
- **PR titles must not include issue numbers** (avoid `Add X (#42)` or `Fix Y — closes #42`). Use `Closes #NN` in the PR body so GitHub links and closes the issue.
- Run the **docs-writer review** (`/document`) only if the issue creates or updates documentation; otherwise skip it and say so in the PR. Always run **`/verify`** before opening a PR.
- PR description starts with a **Main contribution** paragraph
- Human must approve before push or merge

## Notes for Cursor

Read this file at the start of a new agent chat. For documentation work, read `docs-writer.md` and `documentation.mdc`.
