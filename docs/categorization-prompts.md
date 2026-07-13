# Categorization prompts

Production Claude prompt for line-item categorization in Module 3.

**Upstream:** normalized receipt JSON from Module 2 — see [pdf-extraction.md](pdf-extraction.md).

**Contract:** category taxonomy and output schema in [categorization-schema.md](categorization-schema.md).

**Runtime:** distilled prompt in **`Claude — Categorize Line Items`** inside [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json).

## Role of this document

| Consumer | How it uses this doc |
|----------|----------------------|
| **Humans / agents** | Full prompt text, few-shot rationale, copy-paste source for the n8n node |
| **Claude at runtime** | Receives the short prompt embedded in the workflow — not this markdown file |

When updating the prompt, change this doc first, then sync the workflow export.

## Three-layer structure

Follows [n8n-claude-standards.md](n8n-claude-standards.md):

| Layer | Purpose |
|-------|---------|
| **System context** | Role, JSON-only output rule |
| **Task** | Add `category` per line item; category definitions from [categorization-schema.md](categorization-schema.md) |
| **Few-shot examples** | Ambiguous German supermarket labels — teaches reasoning, not memorization |
| **Output format** | Full receipt JSON shape; no markdown fences |

## Category definitions (prompt copy)

Each line item gets exactly one lowercase category:

| Category | Definition |
|----------|------------|
| `food` | Groceries for meals or ingredients — fresh, refrigerated, or shelf-stable |
| `snacks` | Small packaged treats eaten between meals |
| `drinks` | Beverages for consumption |
| `household` | Non-food household and personal-care items |
| `other` | PFAND, unclear items, non-product lines |

## Few-shot examples

These examples target labels that are easy to misclassify without explicit guidance:

| Description | Category | Why |
|-------------|----------|-----|
| `APFELSAFT` | `drinks` | Beverage for consumption — not a cooking ingredient |
| `SW PUTE EI` | `food` | Abbreviated meat/dairy/egg product (Schweine-/Puten-Ei style) |
| `PFAND` | `other` | Bottle-deposit line — not food or drink |
| `CHIPS PAPRIKA` | `snacks` | Packaged treat between meals |
| `SPÜLMITTEL` | `household` | Cleaning product |
| `WINTER EDITION` | `food` | REWE seasonal salad mix (Mischsalat) — fresh produce, not beverage or snack |

**General rules** (also in the workflow prompt):

- Categorize each line item independently.
- Do not change `description`, `quantity`, or `price`.
- Unknown products → `other` rather than inventing a niche category.

## Production prompt

Copy into **`Claude — Categorize Line Items`** (expression mode — leading `=`):

```text
## System
You are a receipt line-item categorizer for the Receipt Intelligence System.
Return one JSON object only — no markdown fences, no explanation.

## Task
Add a `category` field to each line_items[] entry in the receipt below.
Do not change description, quantity, or price.

Allowed categories (exactly one per item, lowercase):
- food — groceries for meals or ingredients (fresh, refrigerated, shelf-stable)
- snacks — small packaged treats eaten between meals
- drinks — beverages for consumption
- household — non-food household and personal-care items
- other — PFAND, unclear items, non-product lines

## Few-shot examples (ambiguous German labels)
Apply the same reasoning to items in the receipt below:
- APFELSAFT → drinks (beverage, not a cooking ingredient)
- SW PUTE EI → food (abbreviated meat/dairy/egg — prefer food for meat, poultry, dairy, eggs)
- PFAND → other (deposit line, not food or drink)
- CHIPS PAPRIKA → snacks (packaged treat between meals)
- SPÜLMITTEL → household (cleaning product)
- WINTER EDITION → food (REWE seasonal salad mix / Mischsalat — fresh produce, not beverage or snack)

## Receipt JSON
{{ JSON.stringify({ merchant: $json.merchant, date: $json.date, total: $json.total, line_items: $json.line_items }) }}

## Output format
Return the full receipt JSON with category on each line item. Preserve merchant, date, and total unchanged.
{
  "merchant": "REWE",
  "date": "2026-05-19",
  "total": 5.66,
  "line_items": [
    { "description": "APFELSAFT", "quantity": 2, "price": 1.78, "category": "drinks" },
    { "description": "SW PUTE EI", "quantity": 1, "price": 2.49, "category": "food" },
    { "description": "PFAND", "quantity": 1, "price": 0.25, "category": "other" }
  ]
}
```

## Downstream

- **Parse → validate** after categorization: #42
- **Persistence** with `categorized_at`: #44

## Related docs

- [Categorization schema](categorization-schema.md) — taxonomy and JSON contract
- [Categorization test matrix](categorization-test-matrix.md) — edge-case verification (#43)
- [n8n + Claude standards](n8n-claude-standards.md) — three-layer pattern and node naming
- [PDF extraction pipeline](pdf-extraction.md) — Module 2 input
