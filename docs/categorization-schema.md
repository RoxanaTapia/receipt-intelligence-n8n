# Categorization schema

Module 3 contract: spending categories and the JSON shape for categorized receipt data.

**Upstream:** normalized receipt JSON from Module 2 — see [pdf-extraction.md](pdf-extraction.md).

**Downstream:** categorization prompts (#41), validation nodes (#42), and persistence (#44) must align with this document.

## Role of this document

This file is the **source of truth** for acceptable categorized output. It is not sent to Claude at runtime.

| Consumer | How it uses this doc |
|----------|----------------------|
| **Prompt author** (#41) | Copies category list, definitions, and output shape into the Claude node prompt |
| **Validator** (#42) | Encodes allowed categories and required fields in a Code node |
| **Verifier / agents** | Checks PRs and workflow output against the contract |

Claude receives a **distilled prompt** (short instructions in the workflow node) plus receipt JSON — not this markdown file.

## Category taxonomy

Each line item gets exactly **one** category. Values are lowercase strings from the table below.

| Category | Definition | Examples |
|----------|------------|----------|
| `food` | Groceries meant as meals or ingredients — fresh, refrigerated, or shelf-stable | Tomaten, Brot, Hähnchen, Milch, Joghurt, Nudeln, Käse |
| `snacks` | Small packaged treats eaten between meals | Chips, Schokolade, Kekse, Gummibärchen, Müsliriegel |
| `drinks` | Beverages for consumption (non-alcoholic in typical supermarket receipts) | Wasser, Apfelsaft, Cola, Kaffee, Tee, Saft |
| `household` | Non-food household and personal-care items | Spülmittel, Waschmittel, Küchenrolle, Shampoo, Seife |
| `other` | Items that do not fit above, or non-product lines that must stay categorized | PFAND (deposit), unclear abbreviations, gift cards |

### Edge-case guidance

Use these rules when writing prompts (#41) and validators (#42):

- **PFAND** → `other` (deposit, not food or drink)
- **Ambiguous abbreviations** (e.g. `SW PUTE EI`) → best-fit category from description; prefer `food` for meat/dairy/egg products
- **Combined receipts** — categorize each line item independently; do not invent new top-level categories
- **Unknown product** — use `other` rather than guessing a niche category

## Output schema

Categorization **extends** the Module 2 receipt shape. All Module 2 fields remain required and unchanged except that each `line_items[]` entry gains a `category` field.

### Required fields (per line item)

| Field | Type | Notes |
|-------|------|-------|
| `description` | string | From Module 2 — unchanged |
| `quantity` | number | From Module 2 — unchanged |
| `price` | number | From Module 2 — unchanged |
| `category` | string | One of: `food`, `snacks`, `drinks`, `household`, `other` |

### Receipt-level fields

| Field | Required | Notes |
|-------|----------|-------|
| `merchant` | Yes | From Module 2 |
| `date` | Yes | `YYYY-MM-DD` |
| `total` | Yes | Final amount paid (EUR) |
| `line_items` | Yes | Non-empty array; every entry must include `category` |
| `extracted_at` | If present on input | Preserved from Module 2 persistence — do not remove |
| `categorized_at` | Optional | ISO-8601 UTC timestamp set at categorization write time (#44) |

### Example (after categorization)

```json
{
  "merchant": "REWE",
  "date": "2024-03-15",
  "extracted_at": "2026-07-07T14:30:00.000Z",
  "total": 8.47,
  "line_items": [
    {
      "description": "Tomaten",
      "quantity": 0.5,
      "price": 1.99,
      "category": "food"
    },
    {
      "description": "APFELSAFT",
      "quantity": 1,
      "price": 2.49,
      "category": "drinks"
    },
    {
      "description": "PFAND",
      "quantity": 1,
      "price": 0.25,
      "category": "other"
    }
  ],
  "categorized_at": "2026-07-07T16:00:00.000Z"
}
```

## Validation rules

Deterministic nodes (#42) should enforce at minimum:

1. Output is a JSON object (after parse step).
2. `merchant`, `date`, `total`, and `line_items` match Module 2 requirements.
3. `line_items` is a non-empty array.
4. Every line item has `category` as a string in the allowed set: `food`, `snacks`, `drinks`, `household`, `other`.
5. No extra categories or alternate spellings (e.g. `Snack`, `beverage`) — reject with `valid: false`.

Follow the same error pattern as Module 2: `valid`, `errors`, `stage` (`"parse"` or `"validation"`).

## Prompt hints (for #41)

When distilling this contract into a Claude prompt, include at minimum:

- The five allowed category names
- One-line definitions (from the taxonomy table)
- Instruction to add `category` to each existing line item without changing `description`, `quantity`, or `price`
- Output format: full receipt JSON, no markdown fences

Few-shot examples for ambiguous German labels: [categorization-prompts.md](categorization-prompts.md).

## Related docs

- [PDF extraction pipeline](pdf-extraction.md) — Module 2 input schema
- [n8n + Claude standards](n8n-claude-standards.md) — prompt structure and parse → validate pattern
- [Categorization prompts](categorization-prompts.md) — production prompt and few-shot examples
- [Agent workflow](../AGENTS.md)
