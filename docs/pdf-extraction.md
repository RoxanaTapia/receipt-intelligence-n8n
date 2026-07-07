# PDF extraction pipeline

Module 2 end-to-end guide: sample PDF → Claude extraction → validated JSON on disk.

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
| Persist | `Set — Normalized Receipt` → `Code — Build Receipt File` → `Write File — Persist Receipt JSON` | Canonical JSON + hash → disk |

## Error path

Parse or validation failures route to **`Set — Validation Error`** (not a retry loop — Module 6 adds hardening):

| Field | Meaning |
|-------|---------|
| `valid` | Always `false` |
| `errors` | Array of error messages |
| `stage` | `"parse"` or `"validation"` |

## Output schema

Required fields after validation:

```json
{
  "merchant": "Muster Supermarkt",
  "date": "2024-03-15",
  "total": 12.34,
  "line_items": [
    { "description": "Tomaten", "quantity": 0.5, "price": 1.99 }
  ]
}
```

Prompt design, domain rules, and the parse → validate pattern: [n8n-claude-standards.md](n8n-claude-standards.md).

## Samples and output

| Topic | Doc |
|-------|-----|
| Sample PDFs, privacy, `docker cp` | [`samples/README.md`](../samples/README.md) |
| File naming, content hash, Docker paths, git policy | [`data/README.md`](../data/README.md) |

Runtime JSON appears on the host at `data/receipts/` (bind-mounted from the container).

## Run locally

1. Start n8n — [n8n-setup.md](n8n-setup.md)
2. Copy a sample PDF and run the workflow — [Run the PDF ingest workflow](n8n-setup.md#run-the-pdf-ingest-workflow)
3. Confirm output in `data/receipts/` on your machine

## Related docs

- [n8n Docker setup](n8n-setup.md)
- [Claude standards](n8n-claude-standards.md)
- [Agent workflow](../AGENTS.md)
