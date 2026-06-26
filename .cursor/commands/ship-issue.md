# /ship-issue Command

You are acting as the **milestone-orchestrator**.

Your task is to fully ship a GitHub issue. **Canonical workflow:** `.cursor/agents/milestone-orchestrator.md` (Delegation, Shipping Phases, Commit summary table, Post-PR handoff, Strict Rules). This command is the entry point — do not duplicate those sections here.

## Instructions

1. **Read the issue** thoroughly and understand the goal.
2. **Check** `AGENTS.md`, `.cursor/rules/elegant-minimal-python.mdc`, and `.cursor/agents/milestone-orchestrator.md`.
3. Create a new branch: `feat/<short-description>`
4. **Coordinate & implement** — orchestrator → **Delegation**, phase 1.
5. **Verify** — run `verifier`; phase 2.
6. **Commit summary** — orchestrator → **Commit summary table**; present with proposed PR; wait for human confirmation; phase 3.
7. **PR** — after confirmation, push and open PR (`Closes #NN`); phase 4. Do **not** push or merge without explicit human approval.
8. **Learn** — orchestrator → **Post-PR handoff**, phase 5.

## Output Expectations

- State the current **phase** (names in orchestrator → Shipping Phases).
- Use the blocker template when stuck.

## Goal

Ship the issue by following the orchestrator agent doc — one source of truth.
