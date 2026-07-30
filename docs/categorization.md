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
  → … (post-persist API — see [setup contract](n8n-setup.md#n8n--api-integration-contract) · [integration.md](integration.md))
```

Categorization ends at **persist**. After a successful write, the same workflow continues into post-persist HTTP (coverage → analytics summary → demo Q&A) — details in [setup](n8n-setup.md#post-persist-coverage-smoke) and the [integration runbook](integration.md).

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

## Error path

Claude categorize allows **at most 3 attempts** (1 initial + 2 retries) for the categorize Claude path. Parse or validation failure with attempts remaining re-invokes **`Claude — Categorize Line Items`** with the receipt rehydrated from **`Set — Normalized Receipt`**. After 3 failures, the run ends on **`Set — Categorization Error`**:

| Field | Meaning |
|-------|---------|
| `valid` | Always `false` |
| `errors` | Array of error messages |
| `stage` | `"parse"` or `"validation"` |

Post-persist API failures use the same shape on separate terminals ([setup failure modes](n8n-setup.md#post-persist-failure-modes)):

| Terminal | `stage` | When |
|----------|---------|------|
| **`Set — API Error`** | `"api"` | Unreachable API, timeout, or 5xx on health / coverage / summary / demo Q&A after bounded HTTP retries |
| **`Set — Empty Coverage`** | `"coverage"` | API responded but zero files loaded or the just-persisted file is missing |

Successful disk persist is never undone by these branches. Retry policy: [setup failure modes](n8n-setup.md#post-persist-failure-modes).

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

| Doc | Role |
|-----|------|
| [Docs index](README.md) | Reading order |
| [pdf-extraction.md](pdf-extraction.md) | Upstream extraction |
| [n8n-setup.md](n8n-setup.md) | Docker setup; post-persist contract |
| [integration.md](integration.md) | Full-stack demo after persist |
| [data/README.md](../data/README.md) | Receipt JSON store |
| [samples/README.md](../samples/README.md) | Sample PDFs |
| [categorization-schema.md](categorization-schema.md) | Taxonomy and output schema |
| [n8n-claude-standards.md](n8n-claude-standards.md) | Claude vs deterministic nodes |
