# AGENTS.md — Receipt Intelligence System

This document describes how we use Cursor agents, rules, and commands in this project.

## Project Vision

Build a clean, production-style system that processes PDF receipts, extracts and categorizes data using Claude, and answers natural language questions about spending and budget.

Main technologies: **n8n** (core) + **Claude** + **FastAPI** (supporting backend).

## Current Focus

- Module 1: Foundations & Environment Setup
- Establishing a strong and enjoyable agentic workflow

## Core Principles

- Keep things simple, readable, and maintainable
- Small, focused functions and changes
- One issue → one branch → one PR
- Prioritize clarity and long-term quality

## Agent Roster

| Role                     | Responsibility                                           | Notes |
|--------------------------|----------------------------------------------------------|-------|
| `milestone-orchestrator` | Coordinates work, manages branches and commits           | Only agent allowed to commit |
| `verifier`               | Reviews quality, runs checks before PR                   | Must run before creating PRs |
| `software-engineering-professor` | Teaches concepts and issues in a learner-friendly way | Use via `/pedagogical-analysis`; does not ship code |
| `docs-writer`            | Creates and maintains clear documentation                | Uses sections, emojis, and Mermaid when helpful |
| `n8n-engineer`           | Designs, reviews, and improves n8n workflows + Claude integration | Main technical specialist for n8n |
| `claude-prompt-engineer` | Drafts and reviews Claude prompts for n8n workflows      | Follows `docs/n8n-claude-standards.md` |

## Workflow

1. Create or pick a GitHub issue on the Project board.
2. *(Optional, learning)* Use `/pedagogical-analysis #NN` before shipping when you want a friendly lecture on what the issue means.
3. Open a new Agent chat and use `/ship-issue #NN`.
4. Follow the rules in `.cursor/rules/elegant-minimal-python.mdc` and this file.
5. The `verifier` runs before a PR is created.
6. Human reviews and approves before pushing or merging.

Project **Status** is handled by GitHub's built-in Project automations (e.g. PR linked → In Progress, PR merged → Done). No custom Actions or repo secrets are required.

## Slash Commands

| Command         | Purpose                                      | Status  |
|-----------------|----------------------------------------------|---------|
| `/ship-issue`            | Ship one GitHub issue end-to-end             | Ready   |
| `/pedagogical-analysis`  | Teach an issue and its concepts (learner mode) | Ready   |
| `/verify`                | Run quality verification on current changes  | Ready   |

## Commit & PR Policy

- Aim for **granular, reviewable commits** (ideally 1–4 per issue).
- Each commit should represent one logical change.
- Only the `milestone-orchestrator` creates commits.
- Run the verifier before creating a PR.
- Every PR must start with a **Main contribution** paragraph.
- Human must approve before pushing or merging.

## Documentation

- Keep `AGENTS.md` reasonably up to date when we add important agents or commands.
- Update documentation when workflows or important decisions change.

### Documentation ownership (per issue)

Each issue owns documentation for **what it ships**. Cross-cutting docs belong to designated capstone issues — do not update them from other PRs.

- **Primary deliverable docs** (e.g. `docs/n8n-setup.md`, `docs/n8n-claude-standards.md`) are committed in the issue that creates them.
- **Capstone docs** (e.g. root `README.md` in #2) are updated only by the issue that owns them.
- **Cross-links** to docs owned by another issue: note the owning issue on GitHub — do not add README or capstone edits from non-owner PRs.
- The orchestrator runs a **documentation handoff** step before the verifier on every `/ship-issue` (see `milestone-orchestrator.md`).

## Notes for Cursor

When starting a new agent chat, read this file to understand the current agents, commands, and workflow.
