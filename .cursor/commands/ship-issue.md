# /ship-issue Command

You are acting as the **milestone-orchestrator**.

Your task is to fully ship a GitHub issue using the workflow defined in `AGENTS.md`.

## Instructions

1. **Read the issue** thoroughly and understand the goal.
2. **Check `AGENTS.md`** and `.cursor/rules/elegant-minimal-python.mdc` before starting.
3. Create a new branch with a clear name: `feat/<short-description>`
4. **Coordinate & implement** — delegate to specialists when the issue scope matches (see `milestone-orchestrator` → Delegation). Specialists draft; **you** commit in granular steps (usually 1–4 per issue).
5. Run the **`verifier`** agent.
6. **Commit summary (required before PR)** — build a table from the branch (`git log main..HEAD`, files per commit). Present it with the proposed PR title/body and **wait for human confirmation** before push/PR.
7. Do **not** push or merge without explicit human approval.

## Commit summary table

After the issue is implemented and verified, auto-assemble from git history:

```markdown
## Commit summary — Issue #NN (confirm to open PR)

| # | Commit | Files | Why (one line) |
|---|--------|-------|----------------|
| 1 | ... | `path/a` | ... |
```

Fill **Why** from commit bodies or a brief rationale. Include the table in the PR description.

## Output Expectations

- State the current **phase**: Coordinate & implement → Verify → **Commit summary** → PR.
- Say which agents you delegated to (if any) at the start of implementation.
- Ask for confirmation **once** before opening the PR (after the summary table).
- If you encounter a blocker, use the blocker template and stop.

## Goal

Conduct the issue: delegate specialist work when needed, commit traceably, confirm via summary table before the PR.
