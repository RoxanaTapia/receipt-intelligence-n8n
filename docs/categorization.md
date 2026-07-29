# Categorization pipeline

End-to-end guide: normalized receipt JSON → Claude categorization → validated categorized JSON on disk.

**Workflow:** [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) (`Receipt — Ingest PDF`)

**Upstream:** PDF extraction and validation — see [pdf-extraction.md](pdf-extraction.md).

## Pipeline overview

```
Manual Trigger
  → … (PDF extraction + validate)
  → Set — Normalized Receipt
  → Claude — Categorize Line Items
  → Code — Parse Categorization JSON
  → IF — Categorization Parse OK
  → Code — Validate Categories
  → IF — Valid Categories
  → Set — Categorized Receipt
  → Code — Build Receipt File
  → Write File — Persist Receipt JSON
  → HTTP Request — GET Health
  → HTTP Request — GET Analytics Receipts
  → Code — Show Coverage Smoke
  → HTTP Request — GET Analytics Summary
  → Code — Show Analytics Summary
  → HTTP Request — POST Demo Questions
  → Code — Show Demo Q&A Answer
```

| Stage | Node | Role |
|-------|------|------|
| Input | `Set — Normalized Receipt` | Validated extracted receipt JSON |
| AI | `Claude — Categorize Line Items` | Add `category` to each `line_items[]` entry |
| Parse | `Code — Parse Categorization JSON` | Parse Claude output; set `parseOk` |
| Branch | `IF — Categorization Parse OK` | Route on `parseOk === true` |
| Validate | `Code — Validate Categories` | Schema + taxonomy check; set `valid` |
| Branch | `IF — Valid Categories` | Route on `valid === true` |
| Retry | `Code — Decide Categorize Retry` → `IF — Categorize Retry` | On parse/validation failure: re-ask Claude up to 3 attempts, else error Set |
| Persist | `Set — Categorized Receipt` → `Code — Build Receipt File` → `Write File — Persist Receipt JSON` | Canonical JSON + hash + timestamps → disk |
| Smoke | `GET Health` → `IF — API Health OK` → `GET Analytics Receipts` → `IF — API Receipts OK` → `Code — Show Coverage Smoke` → `IF — Coverage Present` | Confirm API coverage sees the new file ([setup smoke](n8n-setup.md#post-persist-coverage-smoke)) |
| Analytics | `GET Analytics Summary` → `IF — API Summary OK` → `Code — Show Analytics Summary` | Spending summary for `preset=last_N_days` (`n_days=90`) ([setup analytics](n8n-setup.md#post-persist-analytics-summary)) |
| Demo Q&A | `POST Demo Questions` → `IF — API Questions OK` → `Code — Show Demo Q&A Answer` | Fixed `POST /questions` demo ([setup Q&A](n8n-setup.md#post-persist-demo-qa)) |

## Error path

Claude categorize allows **at most 3 attempts** (1 initial + 2 retries) per workflow run. Parse or validation failure with attempts remaining re-invokes **`Claude — Categorize Line Items`** with the receipt rehydrated from **`Set — Normalized Receipt`**. After 3 failures, the run ends on **`Set — Categorization Error`**:

| Field | Meaning |
|-------|---------|
| `valid` | Always `false` |
| `errors` | Array of error messages |
| `stage` | `"parse"` or `"validation"` |

Post-persist API failures use the same shape on separate terminals ([setup failure modes](n8n-setup.md#post-persist-failure-modes)):

| Terminal | `stage` | When |
|----------|---------|------|
| **`Set — API Error`** | `"api"` | Unreachable API, timeout, or 5xx on health / coverage / summary / demo Q&A |
| **`Set — Empty Coverage`** | `"coverage"` | API responded but zero files loaded or the just-persisted file is missing |

Successful disk persist is never undone by these branches.

## Output schema

Required fields after categorization and persistence:

```json
{
  "date": "2024-03-15",
  "extracted_at": "2026-07-07T14:30:00.000Z",
  "categorized_at": "2026-07-07T16:00:00.000Z",
  "merchant": "REWE",
  "total": 8.47,
  "line_items": [
    {
      "description": "Tomaten",
      "quantity": 0.5,
      "price": 1.99,
      "category": "food"
    }
  ]
}
```

| Field | In filename hash? | Notes |
|-------|-------------------|-------|
| `merchant`, `date`, `total`, `line_items` (incl. `category`) | Yes | Required; validated before persist |
| `extracted_at` | No | ISO-8601 UTC; set at write time |
| `categorized_at` | No | ISO-8601 UTC; set at write time |

**Hash rule:** `category` on each line item is included in the content hash. Identical categories → same filename → overwrite with updated timestamps. Different categories (e.g. Claude drift) → new hash → new file.

Filename pattern, re-runs, and merchant variance: [`data/README.md`](../data/README.md).

## Samples and output

| Topic | Doc |
|-------|-----|
| Category taxonomy and schema | [categorization-schema.md](categorization-schema.md) |
| Production prompt and few-shot examples | [categorization-prompts.md](categorization-prompts.md) |
| Edge-case test matrix | [categorization-test-matrix.md](categorization-test-matrix.md) |
| File naming, content hash, re-run behavior | [data/README.md](../data/README.md) |
| Sample PDFs | [samples/README.md](../samples/README.md) |

Runtime JSON appears on the host at `data/receipts/` (bind-mounted from the container).

## Run locally

1. Start n8n — [n8n-setup.md](n8n-setup.md)
2. Copy a sample PDF and run the workflow — [Run the PDF ingest workflow](n8n-setup.md#run-the-pdf-ingest-workflow)
3. Confirm categorized output in `data/receipts/` — every `line_items[]` entry has `category`; file has `categorized_at`

## Related docs

- [PDF extraction pipeline](pdf-extraction.md) — upstream extraction step
- [n8n Docker setup](n8n-setup.md)
- [Claude standards](n8n-claude-standards.md)
- [Agent workflow](../AGENTS.md)
