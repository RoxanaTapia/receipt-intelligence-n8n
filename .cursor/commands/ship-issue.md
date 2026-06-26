# /ship-issue Command

You are acting as the **milestone-orchestrator**.

Your task is to fully ship a GitHub issue using the workflow defined in `AGENTS.md`.

## Instructions

1. **Read the issue** thoroughly and understand the goal.
2. **Check `AGENTS.md`** and `.cursor/rules/elegant-minimal-python.mdc` before starting.
3. Create a new branch with a clear name: `feat/<short-description>`
4. **Implement** the issue with **granular commits** as you go (usually 1–4 per issue; one logical change each).
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

- State the current **phase**: Implement → Verify → **Commit summary** → PR.
- Ask for confirmation only **once** before opening the PR (after the summary table).
- If you encounter a blocker, use the blocker template and stop.

## Goal

Ship the issue with traceable commits, then pause for a clear summary before the PR — no extra rules files or pre-work plan approval.
