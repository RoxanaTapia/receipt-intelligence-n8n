# Sample receipts

Anonymized PDF fixtures for local ingest workflows, demos, and tests.

## Directory layout

```
samples/
├── README.md           # This file — naming, privacy, usage
└── receipts/           # Committed public-safe PDFs
    ├── 01-food-homedeco.pdf
    ├── 02-vegetables-weighted.pdf
    ├── 03-small.pdf
    ├── 04-article-discount.pdf
    ├── originals/      # Gitignored — pre-anonymization sources (local only)
    └── private/        # Gitignored — other real receipts (local only)
```

Committed samples are **anonymized** copies. Their **original** source PDFs live in `receipts/originals/` on your machine only (never committed). Other ad-hoc real receipts go in `receipts/private/`.

## Sample catalog

| File | Pages | What it demonstrates |
|------|-------|----------------------|
| [03-small.pdf](receipts/03-small.pdf) | 1 | Short receipt with few line items — quick smoke tests |
| [01-food-homedeco.pdf](receipts/01-food-homedeco.pdf) | 2 | Mixed basket: groceries plus non-food (e.g. kitchen utensils) |
| [02-vegetables-weighted.pdf](receipts/02-vegetables-weighted.pdf) | 2 | Produce sold by weight (`kg x price/kg`) |
| [04-article-discount.pdf](receipts/04-article-discount.pdf) | 2 | In-store markdowns (e.g. `Frischerbatt`) |

All samples share common German supermarket patterns useful for extraction testing:

- **Pfand** — deposit on returnable bottles (`PFAND 0,15 EUR`); returned bottles appear as **LEERG. MW V. ST** (Leergut) credits
- **Bonus-Guthaben** — loyalty points applied as a discount on the total
- **Quantity multiples** — same article bought more than once (`2 Stk x …`)
- **Article discounts** — reduced prices marked on individual lines

## Naming conventions

Committed samples use this pattern:

```
NN-<short-description>.pdf
```

| Part | Rule |
|------|------|
| `NN` | Two-digit sort order (`01`, `02`, …) |
| `<short-description>` | Lowercase kebab-case describing what the file tests |
| Extension | Always `.pdf` |

Examples: `03-small.pdf`, `02-vegetables-weighted.pdf`.

Do not commit filenames tied to real store locations, dates, or personal identifiers.

## Privacy rules

Only **anonymized, generic** receipts belong in `samples/receipts/`.

Before adding a new sample, confirm:

- [ ] Store name and address are fictional (e.g. *Musterstadt*, *Musterstraße*)
- [ ] No real names, phone numbers, loyalty IDs, or full payment card numbers
- [ ] Payment blocks use masked or fictional values only
- [ ] Content is safe to show in a public portfolio repo

Real receipts stay in `samples/receipts/private/` on your machine — never commit that folder.

## Original sources (gitignored)

Pre-anonymization PDFs that produced the committed fixtures belong in `samples/receipts/originals/`. Use this naming so each original maps to its public sample:

```
NN-<short-description>_original.pdf
```

| Original (local only) | Anonymized (committed) |
|-----------------------|------------------------|
| `01-food-homedeco_original.pdf` | `01-food-homedeco.pdf` |
| `02-vegetables-weighted_original.pdf` | `02-vegetables-weighted.pdf` |
| `03-small_original.pdf` | `03-small.pdf` |
| `04-article-discount_original.pdf` | `04-article-discount.pdf` |

**Why keep originals locally:** re-run real-world OCR/layout scenarios, refresh anonymized fixtures, and compare extraction drift against authentic receipts — without committing PII to git.

Originals are gitignored and **not** on the Compose samples mount. Copy one into the container only if you need a local operator experiment:

```bash
docker cp samples/receipts/originals/03-small_original.pdf receipt-intelligence-n8n-n8n-1:/home/node/.n8n-files/samples/03-small-original.pdf
```

Prefer committed anonymized samples for the demo webhook allowlist.

## Using samples in the ingest pipeline

1. Start n8n — see [docs/n8n-setup.md](../docs/n8n-setup.md). Compose bind-mounts this folder at `/home/node/.n8n-files/samples` (read-only) — no `docker cp` for committed samples.
2. Import [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json).
3. **Operator:** **Execute workflow** (Manual Trigger) — default sample `03-small`.
4. **Demo / webhook:** activate the workflow and `POST` `{ "sample": "03-small" }` — [Demo sample webhook](../docs/n8n-setup.md#demo-sample-webhook).
5. Confirm categorized JSON under `data/receipts/` — [categorization.md](../docs/categorization.md) · [data/README.md](../data/README.md)
6. Optional full-stack demo (API coverage / analytics / Q&A) — [integration.md](../docs/integration.md)

Allowlisted sample ids match the filename stem (`03-small`, `01-food-homedeco`, …). Unknown ids are rejected by the webhook. Production intake (email, arbitrary upload API, etc.) is out of scope; these fixtures simulate input for reproducible demos.

## Adding a new sample

1. Anonymize the source PDF (fictional address, masked payment details)
2. Name it with the next available `NN-` prefix
3. Add a row to the catalog table above
4. Open a PR — verifier checks paths and privacy rules

## Related docs

| Doc | Role |
|-----|------|
| [Docs index](../docs/README.md) | Reading order |
| [n8n-setup.md](../docs/n8n-setup.md) | Docker setup and ingest how-to |
| [pdf-extraction.md](../docs/pdf-extraction.md) | Extraction pipeline |
| [categorization.md](../docs/categorization.md) | Categorization and persist |
| [data/README.md](../data/README.md) | Receipt JSON store |
| [integration.md](../docs/integration.md) | Full-stack demo |