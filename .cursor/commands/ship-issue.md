# /ship-issue Command

You are acting as the **milestone-orchestrator**.

Ship a GitHub issue using `AGENTS.md` and `.cursor/rules/elegant-minimal-python.mdc`.

## Instructions

1. **Read the issue** and classify acceptance criteria: agent / human / shared.
2. **Plan specialists** — see specialist table in `milestone-orchestrator.md`.
3. **Human checkpoints** — pause using the template in `milestone-orchestrator.md` when required.
4. Create branch: `feat/<short-description>`.
5. **Implement** — granular commits; only the orchestrator commits.
6. **`/document`** — if doc triggers in `.cursor/commands/document.md` match, run docs-writer review, apply edits, commit. Otherwise note skip in PR.
7. **`/verify`** — always before PR.
8. **Open PR** — Main contribution paragraph; `Closes #NN`; human approval before push/merge.

## Output Expectations

- State each step clearly; propose commit messages before committing.
- Ask for confirmation before creating the PR.
- Use human checkpoint or blocker templates when needed.

## Goal

Ship reliably with clean git history and complete documentation handoff.
