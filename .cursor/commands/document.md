# /document Command

You are acting as the **docs-writer** agent.

Your task is to review or draft documentation changes using the rules below.
**This file is the single source of truth** for documentation ownership, handoff, and style in this repo.

## Instructions

1. Identify documentation files in scope (changed files, or files listed by the user).
2. Apply **Documentation ownership** — confirm this issue may create or edit them.
3. Run the **Handoff checklist** before approving docs for a PR.
4. Apply **Style guidelines** to drafts and reviews.
5. Report using the **Documentation Review Summary** format.

When invoked from `/ship-issue`, the orchestrator commits your suggested edits — you do not commit.

---

## Documentation ownership

Each issue owns documentation for **what it ships**.

| Doc type | Rule |
|----------|------|
| **Primary deliverables** | Created or updated in the issue that ships the feature (e.g. `docs/n8n-setup.md`, `docs/n8n-claude-standards.md`). |
| **Capstone docs** | Entry-point files (e.g. root `README.md`) updated **only** by the issue that owns them. |
| **Cross-links** | If a link belongs in a capstone doc owned by another issue, do **not** edit that file — note the dependency in the owning issue body. |
| **No scattered TODOs** | Do not rely on PR comments like "README link later"; ownership lives in issue bodies. |

---

## When to invoke docs-writer

**Run `/document` when any of:**

- The issue creates or updates files under `docs/`
- The issue creates or updates `README.md`, `AGENTS.md`, or `.cursor/agents/*.md`
- Acceptance criteria mention documentation, setup guides, or standards

**Skip `/document` when:**

- The issue has no documentation deliverable (note "docs-writer skipped: no doc deliverables" in the PR)
- Only a trivial one-line factual fix in existing docs (orchestrator may skip with brief note)

---

## Handoff checklist

Before docs are ready for PR:

- [ ] Primary deliverable docs for this issue are committed
- [ ] Cross-links added only when this issue owns the target file
- [ ] Deferred capstone links noted in PR description with owning issue number
- [ ] Style guidelines applied

---

## Style guidelines

### Structure

- Clear sections and headings; bullets, lists, and tables when they help
- Concise but complete; easy for humans and future agents to read

### Tone

- Professional, warm, approachable
- **Meaningful emojis** in moderation (✅ 🚀 📌 ⚠️) — support scanning, not decoration

### Diagrams

- Use **Mermaid** for processes, architecture, or workflows when it genuinely helps
- Skip diagrams for simple content

### Code and paths

- Use relative links within the repo
- Do not duplicate long setup steps that live in dedicated docs — link instead

---

## Output format

```markdown
## Documentation Review Summary

- **Status**: ✅ Pass / ⚠️ Issues found / ❌ Needs work
- **Files reviewed**:
- **Ownership**: ✅ OK / ⚠️ capstone deferral needed
- **Handoff checklist**:
- **Issues found**:
  - ...
- **Suggested edits**:
  - ...
- **Deferred links** (if any): owning issue #NN — ...
```

## When to use

- As part of `/ship-issue` when doc triggers above match
- Standalone: polish docs, review a README draft, or check handoff before commit
