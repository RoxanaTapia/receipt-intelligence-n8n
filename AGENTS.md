# AGENTS.md — Receipt Intelligence System

How we use Cursor agents, rules, and commands in this project.

## Project Vision

Build a clean, production-style system that processes PDF receipts, extracts and categorizes data using Claude, and answers natural language questions about spending and budget.

**Stack:** n8n (core) · Claude · FastAPI (supporting backend)

## Current Focus

- Module 1: Foundations & Environment Setup
- Establishing a strong and enjoyable agentic workflow

## Core Principles

- Keep things simple, readable, and maintainable
- Small, focused functions and changes
- One issue → one branch → one PR
- Prioritize clarity and long-term quality

## Agent Roster

| Role | Responsibility | Notes |
|------|----------------|-------|
| `milestone-orchestrator` | Coordinates shipping, branches, commits | Only agent allowed to commit |
| `docs-writer` | Documentation draft and review | Invoked via `/document`; rules in `document.md` |
| `verifier` | Quality checks before PR | Invoked via `/verify` |
| `software-engineering-professor` | Teaches issues and concepts | `/pedagogical-analysis`; does not ship |
| `n8n-engineer` | n8n workflows and integration | Workflow structure and nodes |
| `claude-prompt-engineer` | Claude prompts in n8n | Follows `docs/n8n-claude-standards.md` |

## Workflow

1. Pick a GitHub issue on the Project board.
2. *(Optional)* `/pedagogical-analysis #NN` — learn before building.
3. `/ship-issue #NN` — orchestrator implements with specialist support.
4. Inside shipping: **`/document`** when doc triggers match → **`/verify`** → PR.
5. Human reviews and approves before push or merge.

Project **Status** uses GitHub Project automations (PR linked → In Progress; merged → Done).

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/ship-issue` | Ship one GitHub issue end-to-end |
| `/document` | Documentation ownership, handoff, style, and review |
| `/verify` | Quality verification before PR |
| `/pedagogical-analysis` | Teach an issue (learner mode) |

**Documentation rules:** `.cursor/commands/document.md` (single source of truth).

## Commit & PR Policy

- Granular, reviewable commits (ideally 1–4 per issue)
- Only `milestone-orchestrator` creates commits
- `/document` when doc triggers match; `/verify` always before PR
- PR description starts with a **Main contribution** paragraph
- Human must approve before push or merge

## Notes for Cursor

Read this file at the start of a new agent chat. For documentation work, read `.cursor/commands/document.md`.
