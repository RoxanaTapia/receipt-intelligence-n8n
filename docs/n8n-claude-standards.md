# n8n + Claude Standards

Guidelines for using Claude inside n8n workflows in the Receipt Intelligence System.

## When to use Claude vs. deterministic nodes

| Use **deterministic nodes** (Set, IF, Code, HTTP Request) | Use **Claude** (AI / HTTP node) |
|-----------------------------------------------------------|----------------------------------|
| Fixed formats, regex, date parsing | Messy or unstructured text (e.g. receipt OCR) |
| Math, filtering, routing by known rules | Semantic judgment (e.g. line-item interpretation) |
| Calling APIs with stable schemas | Natural language or reasoning over text |
| You need fully reproducible output | Fuzzy matching is acceptable with guardrails |

**Rule of thumb:** use Claude to *interpret* ambiguous input; use deterministic nodes to *validate, transform, and route* structured output afterward.

## Prompt structure (three layers)

Every Claude prompt in this project should include three layers. Keep each layer short and explicit.

1. **System context** — role and domain rules.
2. **Task** — what to extract or decide from the input.
3. **Output format** — exact JSON shape for the next n8n node (no markdown fences).

## Parse → validate pattern (Module 2)

After every Claude extraction node, use two deterministic Code nodes:

| Step | Flag | Checks |
|------|------|--------|
| **Parse** | `parseOk` | Non-empty response; valid JSON object |
| **Validate** | `valid` | Required fields; type normalization (dates, numbers) |

Route failures to a **`Set — Validation Error`** node with `valid: false`, `errors`, and `stage` (`"parse"` or `"validation"`). Retry loops are Module 6 — document and route errors; do not silently drop bad output.

See [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) for the reference implementation.

## Domain rules vs few-shot examples

Module 2 uses **domain rules in the prompt** (German supermarket patterns) rather than classic few-shot examples:

- `2 Stk x 0,89` — quantity breakdown for the product line above
- **PFAND** — deposit as its own line item
- Weighted produce — `kg x price/kg` as one item with weight as quantity
- Exclude subtotals, tax, payment, loyalty lines

Few-shot example blocks and retry prompts are deferred to Module 3+ / Module 6.

## Receipt extraction prompt

Production prompt lives in **`Claude — Extract Receipt`** inside [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json). Summary:

| Field | Type | Notes |
|-------|------|-------|
| `merchant` | string | Store name |
| `date` | string | `YYYY-MM-DD` |
| `total` | number | Final amount paid (EUR) |
| `line_items` | array | Each item: `description`, `quantity`, `price` |

Upstream expression: `{{ $json.text }}` from **Extract from File — PDF to Text**.

Full pipeline: [pdf-extraction.md](pdf-extraction.md).

## Node naming conventions

| Node type | Pattern | Example |
|-----------|---------|---------|
| Claude / AI | `Claude — <action>` | `Claude — Extract Receipt` |
| Deterministic transform | `Set — <purpose>` | `Set — Normalized Receipt` |
| Code | `Code — <purpose>` | `Code — Parse Receipt JSON` |
| Branching | `IF — <condition>` | `IF — Parse OK` |
| Trigger | `<type> Trigger` or descriptive name | `Manual Trigger` |

**Workflow names:** scope by purpose, e.g. `Receipt — Ingest PDF`.

Reference workflows:

- [`hello-world.json`](../workflows/hello-world.json) — deterministic-only smoke test
- [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) — Module 2 PDF pipeline with Claude

## Related docs

- [PDF extraction pipeline](pdf-extraction.md)
- [n8n Docker setup](n8n-setup.md)
- [Agent workflow](../AGENTS.md) — includes `claude-prompt-engineer` for prompt drafting and review
