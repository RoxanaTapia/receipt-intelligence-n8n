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
| `milestone-orchestrator` | Coordinates shipping, branches, commits | Only agent allowed to commit; decides when to call specialists |
| `docs-writer` | Documentation draft and review | `/document`; ownership/handoff in agent, style in `documentation.mdc` |
| `verifier` | Quality checks and acceptance criteria before PR | `/verify`; blocks PR if criteria ❌ missing |
| `software-engineering-professor` | Teaches issues and concepts | `/lecture-on-issue`; does not ship |
| `n8n-engineer` | n8n workflows and integration | Workflow structure and nodes |
| `claude-prompt-engineer` | Claude prompts in n8n | Follows `docs/n8n-claude-standards.md` |

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

**Inline vs repo docs:** Docstrings and code comments are part of normal implement work (`elegant-minimal-python.mdc`). Repo markdown (`docs/`, `README.md`, etc.) goes through docs-writer (`/document`) only when the orchestrator's docs-writer triggers match.

## Documentation accuracy

Repo docs must match the codebase today — not aspirational or stale behavior.

| Step | Who | Checks |
|------|-----|--------|
| Draft / review | `docs-writer` | Style, ownership, real paths, link, don't duplicate |
| Technical claims | `n8n-engineer`, `claude-prompt-engineer` | **Consult** when docs describe workflows, nodes, prompts, or schemas — match `workflows/` and shipped prompts |
| Pre-PR gate | `verifier` | Links resolve; doc claims match repo; specialist consult recorded when triggers applied |

Orchestrator invokes specialist consult **before** `/document` on doc issues that describe n8n or Claude behavior (see `milestone-orchestrator.md`).

## Commit & PR Policy

- Granular, reviewable commits (ideally 1–4 per issue)
- Only `milestone-orchestrator` creates commits
- Run the **docs-writer review** (`/document`) only if the issue creates or updates documentation; otherwise skip it and say so in the PR. Always run **`/verify`** before opening a PR.
- PR description starts with a **Main contribution** paragraph
- Human must approve before push or merge

## Notes for Cursor

Read this file at the start of a new agent chat. For documentation work, read `docs-writer.md` and `documentation.mdc`.
