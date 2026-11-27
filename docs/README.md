# Documentation index

Guides for the Receipt Intelligence n8n repo — setup, ingest pipeline, and local full-stack demo.

## Reading order

1. **[n8n-setup.md](n8n-setup.md)** — Start Docker n8n, env vars, import workflows
2. **[pdf-extraction.md](pdf-extraction.md)** — PDF → Claude extract → validated receipt JSON
3. **[categorization.md](categorization.md)** — Categories on line items → persist to disk
4. **[data/README.md](../data/README.md)** — Filename hash, timestamps, re-run behavior
5. **[n8n-setup.md — API contract](n8n-setup.md#n8n--api-integration-contract)** — Shared disk vs HTTP; post-persist steps and failure modes
6. **[integration.md](integration.md)** — Ordered full-stack demo (n8n + API + sample PDF)

For analytics and natural-language Q&A details, use the sibling [receipt-intelligence-api](https://github.com/RoxanaTapia/receipt-intelligence-api) docs (link from the integration runbook).

## By role

| Doc | Role |
|-----|------|
| [n8n-setup.md](n8n-setup.md) | Docker setup, env vars, n8n ↔ API **contract**, ingest how-to |
| [integration.md](integration.md) | **Demo recipe** — start both apps, run a sample, read API output in n8n |
| [pdf-extraction.md](pdf-extraction.md) | Extraction pipeline (through `Set — Normalized Receipt`) |
| [categorization.md](categorization.md) | Categorization pipeline (through persist) |
| [categorization-schema.md](categorization-schema.md) | Spending category taxonomy and output schema |
| [categorization-prompts.md](categorization-prompts.md) | Production categorization prompt and few-shots |
| [categorization-test-matrix.md](categorization-test-matrix.md) | Edge-case verification matrix |
| [n8n-claude-standards.md](n8n-claude-standards.md) | Claude vs deterministic nodes; parse → validate |
| [../data/README.md](../data/README.md) | Receipt JSON store contract |
| [../samples/README.md](../samples/README.md) | Anonymized PDF fixtures and privacy rules |
| [../workflows/](../workflows/) | Version-controlled workflow exports |
| [contributing.md](contributing.md) | Contributors and operators — shipping workflow, module roadmap, project board |

## Related

- Root overview: [../README.md](../README.md)
- Contributors and operators: [contributing.md](contributing.md)
- How a change happens: [../AGENTS.md](../AGENTS.md)
