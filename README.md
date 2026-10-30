# Receipt Intelligence System

You start with a PDF receipt. The workflows in this repo read it, use Claude to pull out the merchant, date, total, and line items, and put a spending category on each line. You get one JSON file per receipt under `data/receipts/`.

When you ask what you spent, the sibling [API](https://github.com/RoxanaTapia/receipt-intelligence-api) reads that folder and answers. The [demo](https://github.com/RoxanaTapia/receipt-intelligence-demo) is where you run the workflows and the API together.

```text
PDF receipt → extract → categorize → data/receipts/*.json
                                      ↓
                         analytics + natural-language Q&A
```

n8n runs the workflows. It writes the categorized JSON to disk. The API reads the same folder through `RECEIPT_DATA_PATH`.

After a file is saved, the ingest workflow checks coverage in one specific way:

- **What is checked.** The API's list of receipt files loaded from that folder. The check passes only when the list is not empty and includes the file just written. Line items, categories, and totals are already settled before this step.
- **When it passes.** The workflow loads an analytics summary and posts one fixed demo question.
- **When it fails.** An empty list, or a list that omits the new file, stops the workflow before that summary and question. The JSON file stays on disk.
- **How the API gets the receipt.** As that file on disk. The workflow does not upload the JSON to the API.

**Demo recipe:** [docs/integration.md](docs/integration.md). **Contract:** [docs/n8n-setup.md](docs/n8n-setup.md#n8n--api-integration-contract). **Coverage check:** [docs/n8n-setup.md](docs/n8n-setup.md#post-persist-coverage-smoke).

## Getting started

1. Clone this repo. Clone the API repo as well if you want the full demo.
2. Start local n8n — [docs/n8n-setup.md](docs/n8n-setup.md) (copy `.env.example` to `.env`, then `docker compose up -d`).
3. Import [workflows/hello-world.json](workflows/hello-world.json) and run it once so you know the editor works.
4. Run the full demo — [docs/integration.md](docs/integration.md).

| Environment | Guide |
|-------------|--------|
| Local n8n | [docs/n8n-setup.md](docs/n8n-setup.md) |
| Local n8n + API | [docs/integration.md](docs/integration.md) |
| Hosted demo | [receipt-intelligence-demo](https://github.com/RoxanaTapia/receipt-intelligence-demo) |

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Engine + Compose v2). The full demo also needs Python 3.11+ for the API.

## Documentation

Start with the [docs index](docs/README.md) for reading order.

**Pipeline path:** [PDF extraction](docs/pdf-extraction.md) → [categorization](docs/categorization.md) → [data store](data/README.md) → [setup contract](docs/n8n-setup.md#n8n--api-integration-contract) → [integration runbook](docs/integration.md).

| Area | Resource | Description |
|------|----------|-------------|
| Docs index | [docs/README.md](docs/README.md) | Reading order and roles |
| Setup | [docs/n8n-setup.md](docs/n8n-setup.md) | Docker n8n, env vars, n8n ↔ API contract |
| Integration | [docs/integration.md](docs/integration.md) | Local full-stack demo (n8n + API + sample PDF) |
| Extraction | [docs/pdf-extraction.md](docs/pdf-extraction.md) | PDF → Claude → validated JSON |
| Categorization | [docs/categorization.md](docs/categorization.md) | Categories on line items → JSON on disk |
| Schema / prompts / tests | [schema](docs/categorization-schema.md) · [prompts](docs/categorization-prompts.md) · [matrix](docs/categorization-test-matrix.md) | Taxonomy, few-shots, edge cases |
| Standards | [docs/n8n-claude-standards.md](docs/n8n-claude-standards.md) | When to use Claude vs deterministic nodes |
| Data store | [data/README.md](data/README.md) | Filenames, content hash, re-runs |
| Samples | [samples/README.md](samples/README.md) | Anonymized PDF fixtures |
| Workflows | [workflows/](workflows/) | Version-controlled n8n exports |

## Repository structure

```
receipt-intelligence-n8n/
├── AGENTS.md                 # Contributor guide
├── .cursor/                  # Editor configuration
├── docker-compose.yml        # Self-hosted n8n
├── .env.example              # Environment variable template
├── docs/
│   ├── README.md             # Docs index and reading order
│   ├── contributing.md       # Notes for contributors and operators
│   ├── n8n-setup.md          # Local Docker setup + API contract
│   ├── integration.md        # Full-stack demo runbook
│   ├── n8n-claude-standards.md
│   ├── pdf-extraction.md
│   ├── categorization.md
│   ├── categorization-schema.md
│   ├── categorization-prompts.md
│   └── categorization-test-matrix.md
├── samples/
│   ├── README.md             # Anonymized PDF catalog and privacy rules
│   └── receipts/             # Committed public-safe PDF fixtures
├── data/
│   ├── README.md             # Receipt JSON store contract
│   └── receipts/             # Categorized JSON output (runtime)
└── workflows/
    ├── hello-world.json
    └── receipt-pdf-ingest.json
```

## Contributors

If you change this repo or run it locally, start at [docs/contributing.md](docs/contributing.md).
