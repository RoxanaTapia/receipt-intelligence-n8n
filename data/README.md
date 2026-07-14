# Receipt data store

Categorized receipt JSON written by the [`receipt-pdf-ingest`](../workflows/receipt-pdf-ingest.json) workflow after Claude extraction, validation, categorization, and persistence (#44).

## Directory layout

```
data/
├── README.md                 # This file
└── receipts/
    ├── example.json          # Committed showcase (anonymized, Module 2 shape)
    ├── {date}_{slug}_{hash}.json   # Runtime outputs (gitignored)
    └── private/              # Real receipt JSON (gitignored)
```

## File naming

Runtime files use a hybrid pattern:

```
{YYYY-MM-DD}_{merchant_slug}_{content_hash}.json
```

**Example:** `2024-03-15_rewe_a1b2c3d4.json`

| Part | Rule |
|------|------|
| Date | Normalized `YYYY-MM-DD` from validation |
| Slug | Lowercase merchant; accents stripped; non-alphanumeric → `-`; max 40 chars |
| Hash | First 8 hex chars of `SHA256(canonical_json)` |

### Content hash

The hash is computed from **canonical JSON** — not Claude's raw output:

- Keys in order: `date`, `line_items`, `merchant`, `total`
- `line_items` sorted by `description`
- Each line item includes `category`, `description`, `price`, `quantity` (keys in that order)
- Compact `JSON.stringify` (no pretty-print) for hashing
- **`extracted_at` and `categorized_at` are excluded** — write timestamps do not affect the hash or filename

| Behavior | |
|----------|--|
| Identical receipt + categories → same hash | File **overwritten** in place; `extracted_at` and `categorized_at` updated |
| Any change in extracted data or categories | New hash → **new file** (previous file remains) |

### Re-runs and multiple files

The filename date is the **receipt transaction date**, not the run time. The middle segment is a **merchant slug**; the suffix is a **content hash** of `date`, `line_items` (with `category`), `merchant`, and `total`.

`extracted_at` and `categorized_at` are stored **inside** the JSON only — they never appear in the filename and are excluded from the hash.

**Common causes of multiple files for one PDF:**

| Cause | Effect |
|-------|--------|
| Merchant name variance (`"REWE"` vs `"REWE Markt"`) | Different slug **and** hash → two files |
| Line-item extraction variance | Different hash → new file |
| Category drift on re-run | Different hash → new file (category is in the hash) |

| Question | How to answer it |
|----------|------------------|
| Which file is from my latest run? | Check `categorized_at` inside the file, or `ls -lt data/receipts/*.json` |
| Why two files for one receipt? | Usually unstable `merchant`, line items, or categories from Claude |
| Can I clean up old runs? | Delete stale hash-named files locally (gitignored) |

## Docker paths

n8n runs in Docker. The workflow writes to the **container** path; a bind mount mirrors it to this repo on your Mac.

| Context | Path |
|---------|------|
| Host (repo) | `data/receipts/` |
| Container (Write File node) | `/home/node/.n8n-files/receipts/` |

Configured in [`docker-compose.yml`](../docker-compose.yml):

```yaml
environment:
  NODE_FUNCTION_ALLOW_BUILTIN: crypto   # SHA-256 content hash in Code node
volumes:
  - n8n_data:/home/node/.n8n                        # named volume — n8n app data
  - ./data/receipts:/home/node/.n8n-files/receipts  # bind mount — receipt JSON
```

### Named volume vs bind mount

| | Named volume `n8n_data` | Bind mount `./data/receipts` |
|--|-------------------------|------------------------------|
| Stores | n8n SQLite DB, credentials, encryption key | Receipt JSON outputs |
| Visible in repo | No | Yes |

See [n8n setup](../docs/n8n-setup.md) for Docker restart steps after compose changes.

## Git policy

| Path | Committed? | Purpose |
|------|------------|---------|
| `data/receipts/*.json` (hash-named) | No | Runtime workflow outputs |
| [`receipts/example.json`](receipts/example.json) | **Yes** | Showcase fixture (Module 2 shape; no categories) |
| `data/receipts/private/` | No | Real receipt JSON from local runs |

### Refresh the showcase

1. Run the workflow on a [sample PDF](../samples/receipts/).
2. Copy the hash-named categorized output to a local file (or update `example.json` if you want a categorized showcase).
3. Verify the content is anonymized (no real store names, addresses, or personal data).
4. Commit only intentional showcase files.

The workflow never auto-overwrites `example.json`.

## JSON shape

Runtime files are **categorized** receipt objects:

```json
{
  "date": "2024-03-15",
  "extracted_at": "2026-07-07T14:30:00.000Z",
  "categorized_at": "2026-07-07T16:00:00.000Z",
  "line_items": [
    {
      "description": "Tomaten",
      "quantity": 0.5,
      "price": 1.99,
      "category": "food"
    }
  ],
  "merchant": "Muster Supermarkt",
  "total": 12.34
}
```

| Field | In content hash? | Notes |
|-------|------------------|-------|
| `merchant`, `date`, `total`, `line_items` (incl. `category`) | Yes | Required; validated before persist |
| `extracted_at` | No | ISO-8601 UTC; set at write time; updates on overwrite |
| `categorized_at` | No | ISO-8601 UTC; set at write time; updates on overwrite |

Required fields match validation in the ingest workflow: `merchant`, `date`, `total`, non-empty `line_items` with `category` on every entry.

## Related docs

- [Categorization pipeline](../docs/categorization.md) — Module 3 persist path
- [Categorization schema](../docs/categorization-schema.md) — taxonomy and output contract
- [Sample PDFs](../samples/README.md) — input fixtures for the pipeline
- [n8n setup](../docs/n8n-setup.md) — Docker, import workflow, copy PDFs into the container
