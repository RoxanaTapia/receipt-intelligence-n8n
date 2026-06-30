# /document Command

You are acting as the **docs-writer** agent.

Review or draft documentation changes for the files in scope.

## Instructions

1. Follow `.cursor/agents/docs-writer.md` for ownership, handoff, triggers, and output format.
2. Apply markdown style from `.cursor/rules/documentation.mdc`.
3. When invoked from `/ship-issue`, the orchestrator commits your suggested edits — you do not commit.

## When to use

- As part of `/ship-issue` when doc triggers in `docs-writer.md` match
- Standalone: polish docs, review a README draft, or check handoff before commit
