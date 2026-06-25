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
| `docs-writer`            | Creates and maintains clear documentation                | Uses sections, emojis, and Mermaid when helpful |
| `n8n-engineer`           | Designs, reviews, and improves n8n workflows + Claude integration | Main technical specialist for n8n |

## Workflow

1. Create or pick a GitHub issue on the Project board.
2. Open a new Agent chat and use `/ship-issue #NN`.
3. Follow the rules in `.cursor/rules/elegant-minimal-python.mdc` and this file.
4. The `verifier` runs before a PR is created.
5. Human reviews and approves before pushing or merging.

Project **Status** is handled by GitHub's built-in Project automations (e.g. PR linked → In Progress, PR merged → Done). No custom Actions or repo secrets are required.

## Slash Commands

| Command         | Purpose                                      | Status  |
|-----------------|----------------------------------------------|---------|
| `/ship-issue`   | Ship one GitHub issue end-to-end             | Ready   |
| `/verify`       | Run quality verification on current changes  | Ready   |

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

## Notes for Cursor

When starting a new agent chat, read this file to understand the current agents, commands, and workflow.
