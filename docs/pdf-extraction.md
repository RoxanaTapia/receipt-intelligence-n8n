# PDF extraction pipeline

End-to-end guide: sample PDF → Claude extraction → validated receipt JSON.

**Workflow:** [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) (`Receipt — Ingest PDF`)

## Pipeline overview

```
Manual Trigger
  → Read Binary File — Sample Receipt
  → Extract from File — PDF to Text
  → Claude — Extract Receipt
  → Code — Parse Receipt JSON
  → IF — Parse OK
  → Code — Validate & Normalize Receipt
  → IF — Valid Receipt
  → Set — Normalized Receipt
  → … (categorization — see [categorization.md](categorization.md))
```

PDF extraction ends at **`Set — Normalized Receipt`**. The full ingest workflow continues into categorization and persistence — see [categorization.md](categorization.md).

**Historical persist path** (before categorization was added):

```
Set — Normalized Receipt
  → Code — Build Receipt File
  → Write File — Persist Receipt JSON
```

| Stage | Node | Role |
|-------|------|------|
| Input | `Read Binary File — Sample Receipt` | Load PDF from `/home/node/.n8n-files/` |
| Text | `Extract from File — PDF to Text` | PDF → plain text (`$json.text`) |
| AI | `Claude — Extract Receipt` | Receipt text → JSON object |
| Parse | `Code — Parse Receipt JSON` | Parse Claude output; set `parseOk` |
| Branch | `IF — Parse OK` | Route on `parseOk === true` |
| Validate | `Code — Validate & Normalize Receipt` | Schema check + normalization; set `valid` |
| Branch | `IF — Valid Receipt` | Route on `valid === true` |
| Retry | `Code — Decide Extract Retry` → `IF — Extract Retry` | On parse/validation failure: re-ask Claude up to 3 attempts, else error Set |
| Output | `Set — Normalized Receipt` | Validated extracted JSON; input to categorization |

## Error path

Claude extract allows **at most 3 attempts** (1 initial + 2 retries) for the extract Claude path. Parse or validation failure with attempts remaining re-invokes **`Claude — Extract Receipt`** with text rehydrated from **`Extract from File — PDF to Text`**. After 3 failures, the run ends on **`Set — Validation Error`**:

| Field | Meaning |
|-------|---------|
| `valid` | Always `false` |
| `errors` | Array of error messages |
| `stage` | `"parse"` or `"validation"` |

## Output schema

Required fields after validation:

```json
{
  "date": "2024-03-15",
  "extracted_at": "2026-07-07T14:30:00.000Z",
  "merchant": "Muster Supermarkt",
  "total": 12.34,
  "line_items": [
    { "description": "Tomaten", "quantity": 0.5, "price": 1.99 }
  ]
}
```

| Field | In filename hash? | Notes |
|-------|-------------------|-------|
| `merchant`, `date`, `total`, `line_items` | Yes | Required; validated before persist |
| `extracted_at` | No | ISO-8601 UTC; set at write time (#36) |

Filename pattern, re-runs, and merchant variance: [`data/README.md`](../data/README.md).

## Samples and output

| Topic | Doc |
|-------|-----|
| Sample PDFs, privacy, `docker cp` | [`samples/README.md`](../samples/README.md) |
| File naming, content hash, `extracted_at`, re-run behavior | [`data/README.md`](../data/README.md) |

Runtime JSON from the full pipeline (categorized) appears on the host at `data/receipts/` — see [categorization.md](categorization.md).

## Run locally

1. Start n8n — [n8n-setup.md](n8n-setup.md)
2. Copy a sample PDF and run the workflow — [Run the PDF ingest workflow](n8n-setup.md#run-the-pdf-ingest-workflow)
3. Confirm output in `data/receipts/` on your machine

## Related docs

- [n8n Docker setup](n8n-setup.md)
- [Claude standards](n8n-claude-standards.md)
- [Categorization pipeline](categorization.md) — downstream categorization step
- [Agent workflow](../AGENTS.md)
