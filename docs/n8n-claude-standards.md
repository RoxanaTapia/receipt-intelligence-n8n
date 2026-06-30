# n8n + Claude Standards

Initial guidelines for using Claude inside n8n workflows in the Receipt Intelligence System.

> **Module 1 foundation** — this doc will grow in Module 2 and 3 as we add real receipt processing, error handling, and evaluation patterns.

## When to use Claude vs. deterministic nodes

| Use **deterministic nodes** (Set, IF, Code, HTTP Request) | Use **Claude** (AI / HTTP node) |
|-----------------------------------------------------------|----------------------------------|
| Fixed formats, regex, date parsing | Messy or unstructured text (e.g. receipt OCR) |
| Math, filtering, routing by known rules | Semantic judgment (e.g. spending category) |
| Calling APIs with stable schemas | Natural language or reasoning over text |
| You need fully reproducible output | Fuzzy matching is acceptable with guardrails |

**Rule of thumb:** use Claude to *interpret* ambiguous input; use deterministic nodes to *validate, transform, and route* structured output afterward.

## Prompt structure (three layers)

Every Claude prompt in this project should include three layers. Keep each layer short and explicit.

1. **System context** — role and domain rules.
   - Who is Claude in this workflow? What constraints apply?
   - Example: *"You are a receipt parser for a personal finance app. Categories: Groceries, Dining, Transport, Other."*

2. **Task** — what to do with this input.
   - Example: *"Extract merchant, date, total, and category from the receipt text below."*

3. **Output format** — how the answer must look for the next n8n node.
   - Example: *"Return valid JSON only, no markdown fences."*

Module 2 will add few-shot examples, retry prompts, and schema validation patterns.

## Node naming conventions

Clear names make visual workflows readable. Use a prefix that shows the node's role.

| Node type | Pattern | Example |
|-----------|---------|---------|
| Claude / AI | `Claude — <action>` | `Claude — Extract Receipt` |
| Deterministic transform | `Set — <purpose>` | `Set — Normalize Date` |
| Branching | `IF — <condition>` | `IF — Has PDF Binary` |
| Trigger | `<type> Trigger` or descriptive name | `Manual Trigger`, `Webhook — PDF Upload` |

**Workflow names:** scope by purpose, e.g. `Receipt — Ingest PDF`, not `Workflow 3`.

See [`workflows/hello-world.json`](../workflows/hello-world.json) for a deterministic-only example (no Claude nodes yet).

## Example prompt template (stub)

Stub for future receipt extraction. Replace `{{ $json.receipt_text }}` with the expression your n8n node uses for upstream data.

```text
## System
You are a receipt data extractor for the Receipt Intelligence System.
Return structured JSON only. Use EUR as default currency unless stated otherwise.

## Task
From the receipt text below, extract:
- merchant (string)
- date (ISO 8601, YYYY-MM-DD)
- total (number)
- category (one of: Groceries, Dining, Transport, Other)

## Receipt text
{{ $json.receipt_text }}

## Output format
Respond with JSON only, no markdown:
{
  "merchant": "...",
  "date": "YYYY-MM-DD",
  "total": 0.00,
  "category": "..."
}
```

## Related docs

- [n8n Docker setup](n8n-setup.md)
- [Agent workflow](../AGENTS.md) — includes the `claude-prompt-engineer` agent for prompt drafting and review
