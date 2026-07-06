# Receipt data store

Validated receipt JSON written by the [`receipt-pdf-ingest`](../workflows/receipt-pdf-ingest.json) workflow after Claude extraction and schema validation (#27).

## Directory layout

```
data/
├── README.md                 # This file
└── receipts/
    ├── example.json          # Committed showcase (anonymized)
    ├── {date}_{slug}_{hash}.json   # Runtime outputs (gitignored)
    └── private/              # Real receipt JSON (gitignored)
```

## File naming

Runtime files use a hybrid pattern:

```
{YYYY-MM-DD}_{merchant_slug}_{content_hash}.json
```

**Example:** `2024-03-15_muster-supermarkt_903b7f35.json`

| Part | Rule |
|------|------|
| Date | Normalized `YYYY-MM-DD` from validation |
| Slug | Lowercase merchant; accents stripped; non-alphanumeric → `-`; max 40 chars |
| Hash | First 8 hex chars of `SHA256(canonical_json)` |

### Content hash

The hash is computed from **canonical JSON** — not Claude's raw output:

- Keys in order: `date`, `line_items`, `merchant`, `total`
- `line_items` sorted by `description`
- Compact `JSON.stringify` (no pretty-print) for hashing

| Behavior | |
|----------|--|
| Same extraction → same filename | File **overwritten** in place |
| Model/prompt change → different JSON | New hash, new file |

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
| [`receipts/example.json`](receipts/example.json) | **Yes** | Showcase fixture for clients |
| `data/receipts/private/` | No | Real receipt JSON from local runs |

### Refresh the showcase

1. Run the workflow on a [sample PDF](../samples/receipts/).
2. Copy the hash-named output to `example.json`.
3. Verify the content is anonymized (no real store names, addresses, or personal data).
4. Commit only `example.json`.

The workflow never auto-overwrites `example.json`.

## JSON shape

Each file is one normalized receipt object:

```json
{
  "date": "2024-03-15",
  "line_items": [
    { "description": "Tomaten", "quantity": 0.5, "price": 1.99 }
  ],
  "merchant": "Muster Supermarkt",
  "total": 12.34
}
```

Required fields match validation in the ingest workflow: `merchant`, `date`, `total`, non-empty `line_items`.

## Related docs

- [Sample PDFs](../samples/README.md) — input fixtures for the pipeline
- [n8n setup](../docs/n8n-setup.md) — Docker, import workflow, copy PDFs into the container
