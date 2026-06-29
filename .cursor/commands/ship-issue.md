# /ship-issue Command

You are acting as the **milestone-orchestrator**.

Your task is to fully ship a GitHub issue using the workflow defined in `AGENTS.md`.

## Instructions

1. **Read the issue** thoroughly and understand the goal.
2. **Check `AGENTS.md`** and `.cursor/rules/elegant-minimal-python.mdc` before starting.
3. **Plan human checkpoints** — classify acceptance criteria as agent / human / shared. If the issue lists a **Human checkpoints** section, pause at each step using the template in `milestone-orchestrator.md` (do not skip UI or local verification the human must perform).
4. Create a new branch with a clear name: `feat/<short-description>`
5. Work on the issue following the rules:
   - Make small, focused, granular commits.
   - Use the `verifier` agent before creating a PR.
   - Only you (the orchestrator) are allowed to commit.
   - Do **not** commit workflow JSON or close verification-dependent work until the human confirms local checks when the issue requires it.
6. Before creating the PR, make sure:
   - All changes are clean and follow the coding standards.
   - The PR description starts with a **Main contribution** paragraph.
   - The PR closes the issue (`Closes #NN`).
7. Do **not** push or merge without explicit human approval.

## Output Expectations

- Clearly communicate what you are doing at each step.
- Propose commit messages before committing.
- Ask for confirmation before creating the PR.
- If you encounter a blocker, use the blocker template and stop.
- At planned human checkpoints, use the **human checkpoint** template from `milestone-orchestrator.md` and wait for the human to reply before continuing.

## Goal

Ship the issue reliably, with clean git history and high code quality.