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
| `milestone-orchestrator` | Coordinates work, manages branches and commits           | Delegates to specialists; only agent allowed to commit |
| `verifier`               | Reviews quality, runs checks before PR                   | Invoked by orchestrator before PR |
| `software-engineering-professor` | Teaches concepts and issues in a learner-friendly way | Use via `/pedagogical-analysis`; does not ship code |
| `docs-writer`            | Creates and maintains clear documentation                | Invoked by orchestrator for doc-heavy issues; does not commit |
| `n8n-engineer`           | Designs, reviews, and improves n8n workflows + Claude integration | Invoked by orchestrator for n8n issues; does not commit |

## Workflow

1. Create or pick a GitHub issue on the Project board.
2. *(Optional)* `/pedagogical-analysis #NN` before shipping.
3. `/ship-issue #NN` — follow `.cursor/agents/milestone-orchestrator.md` (phases, delegation, commit summary before PR).
4. Human approves push and merge.

Project **Status** is handled by GitHub's built-in Project automations (e.g. PR linked → In Progress, PR merged → Done). No custom Actions or repo secrets are required.

## Slash Commands

| Command         | Purpose                                      | Status  |
|-----------------|----------------------------------------------|---------|
| `/ship-issue`            | Ship one GitHub issue end-to-end             | Ready   |
| `/pedagogical-analysis`  | Teach an issue and its concepts (learner mode) | Ready   |
| `/verify`                | Run quality verification on current changes  | Ready   |

## Commit & PR Policy

- Granular commits (ideally 1–4 per issue); delegation and phases → `milestone-orchestrator`.
- Commit summary table from branch history; human confirms once before PR.
- Verifier before PR; **Main contribution** in PR body; human approves push/merge.

## Documentation

- Keep `AGENTS.md` reasonably up to date when we add important agents or commands.
- Update documentation when workflows or important decisions change.

## Notes for Cursor

When starting a new agent chat, read this file to understand the current agents, commands, and workflow.
