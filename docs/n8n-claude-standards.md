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

On parse or validation failure, the workflow retries the same Claude node up to **3 attempts** (1 initial + 2 retries) per Claude path — extract and categorize each have their own bound; parse and validation share that counter — then routes to a **`Set — Validation Error`** (extract) or **`Set — Categorization Error`** (categorize) node with `valid: false`, `errors`, and `stage` (`"parse"` or `"validation"`). Never silently drop bad output.

See [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) for the reference implementation (`Code — Decide Extract Retry` / `Code — Decide Categorize Retry`).

## Domain rules vs few-shot examples

Module 2 uses **domain rules in the prompt** (German supermarket patterns) rather than classic few-shot examples:

- `2 Stk x 0,89` — quantity breakdown for the product line above
- **PFAND** — deposit as its own line item
- Weighted produce — `kg x price/kg` as one item with weight as quantity
- Exclude subtotals, tax, payment, loyalty lines
- **Merchant** — primary store brand only (e.g. `REWE`, not `REWE Markt`) for consistent filenames

Module 3 categorization uses **few-shot examples** for ambiguous product labels — see [categorization-prompts.md](categorization-prompts.md). Retries re-ask with the same production prompt (no separate retry prompt yet).

## Receipt extraction prompt

Production prompt lives in **`Claude — Extract Receipt`** inside [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json). Summary:

| Field | Type | Notes |
|-------|------|-------|
| `merchant` | string | Primary store brand — short consistent form |
| `date` | string | `YYYY-MM-DD` |
| `total` | number | Final amount paid (EUR) |
| `line_items` | array | Each item: `description`, `quantity`, `price` |

Upstream expression: `{{ $json.text }}` from **Extract from File — PDF to Text**.

Full pipeline: [pdf-extraction.md](pdf-extraction.md).

## Line item categorization (Module 3)

Module 3 adds a **`category`** field to each `line_items[]` entry using Claude semantic judgment on normalized receipt JSON.

| Topic | Doc |
|-------|-----|
| Category taxonomy and output schema | [categorization-schema.md](categorization-schema.md) |
| Production prompt and few-shot examples | [categorization-prompts.md](categorization-prompts.md) |
| Parse → validate after categorization | Same pattern as Module 2 — validator checks allowed categories (#42) |

Allowed categories: `food`, `snacks`, `drinks`, `household`, `other`.

### Categorization prompt

Production prompt with few-shot examples lives in **`Claude — Categorize Line Items`** inside [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json). Full text and rationale: [categorization-prompts.md](categorization-prompts.md). Runs after **`Set — Normalized Receipt`**, takes normalized receipt JSON, and adds `category` to each line item per [categorization-schema.md](categorization-schema.md). Parse → validate → persist: [categorization.md](categorization.md).

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
- [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) — Module 2 PDF extraction + Module 3 categorization Claude nodes

## Module 4 — Q&A routing (API)

Natural-language budget questions are routed in [receipt-intelligence-api](https://github.com/RoxanaTapia/receipt-intelligence-api), not inside n8n. Keep the same Claude vs deterministic split:

| Use **Claude** | Use **deterministic code** (FastAPI / Pydantic) |
|----------------|--------------------------------------------------|
| Intent + synonym / time-phrase extraction | Validate routed JSON against `AnalyticsQuery` |
| Friendly narration of analytics *facts* | Aggregation, shares, averages — never invent amounts |
| Insight prose over structured heuristics | Threshold checks and numeric summaries |

**Three-layer prompts** still apply (system / task / output). Routing and narration prompts, intent types, category synonyms, and few-shots live in the API guide:

→ [question-answering.md](https://github.com/RoxanaTapia/receipt-intelligence-api/blob/main/docs/question-answering.md) *(routing + narration contract)*

**Grounding rule:** Claude may interpret the *question*; spend figures come only from the analytics layer. On empty data or validation failure, refuse — do not guess totals.

## Related docs

- [PDF extraction pipeline](pdf-extraction.md)
- [Categorization pipeline](categorization.md)
- [Categorization schema](categorization-schema.md)
- [Categorization prompts](categorization-prompts.md)
- [Categorization test matrix](categorization-test-matrix.md)
- [n8n Docker setup](n8n-setup.md)
- [How a change happens](../AGENTS.md)
- [API Q&A routing](https://github.com/RoxanaTapia/receipt-intelligence-api/blob/main/docs/question-answering.md) — Module 4 intent → analytics
