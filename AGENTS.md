# Project guide

## What we're building

These are the n8n workflows behind the Receipt Intelligence demo at [receipt-intelligence-demo](https://github.com/RoxanaTapia/receipt-intelligence-demo). A workflow reads a PDF receipt, asks Claude for the merchant, date, total, and line items, puts a spending category on each line, and writes one JSON file under `data/receipts/`. The sibling [API](https://github.com/RoxanaTapia/receipt-intelligence-api) reads that folder. Start with [README.md](README.md).

## How a change happens

1. **One issue.** The issue is the request. Use [.github/ISSUE_TEMPLATE.md](.github/ISSUE_TEMPLATE.md). The title starts with one emoji code, such as 🛠️ or 📄.
2. **One branch.** Use a plain descriptive name so this work stays separate from other work.
3. **One pull request.** The title is a plain sentence. The body follows [.github/pull_request_template.md](.github/pull_request_template.md) and includes `Closes #` with the issue number.
4. **Automated tests.** They run on every pull request and on every push to main.
5. **Roxana reviews and merges.**

## Where things are

| Path | What it is |
|---|---|
| [README.md](README.md) | What the workflows do |
| [docs/README.md](docs/README.md) | Reading order for the guides |
| [docs/n8n-setup.md](docs/n8n-setup.md) | Local n8n and the API contract |
| [docs/integration.md](docs/integration.md) | Run n8n and the API together |
| [docs/pdf-extraction.md](docs/pdf-extraction.md) | PDF to validated receipt JSON |
| [docs/categorization.md](docs/categorization.md) | Categories on each line |
| [docs/contributing.md](docs/contributing.md) | Notes for people who ship or run this locally |
| [workflows/](workflows/) | Exported workflows: hello-world and receipt-pdf-ingest |
| [data/README.md](data/README.md) | Receipt JSON written to disk |
| [samples/README.md](samples/README.md) | Sample receipt PDFs |
| [samples/po/](samples/po/) | Sample purchase-order PDFs and their answer key |
| [docker-compose.yml](docker-compose.yml) | Local n8n |
| [.env.example](.env.example) | Env names. Real secrets stay in `.env`, which is not committed |
| [tests/](tests/) | Automated tests |
| [.github/workflows/tests.yml](.github/workflows/tests.yml) | The same tests on GitHub |
| [.cursor/rules/](.cursor/rules/) | Rules for agents |
| [pyproject.toml](pyproject.toml) | Ruff settings |
| [LICENSE](LICENSE) | MIT license |

## Tests

From the repo root:

```bash
python -m unittest discover -s tests -v
python -m pip install ruff
ruff check .
ruff format --check .
```

The unit tests check the purchase-order samples. They also check that every file in `workflows/` parses and holds no embedded credential. GitHub Actions runs these commands on every pull request and on every push to main.

## For the agents

Do:

- Read this guide and `.cursor/rules/` before you edit.
- Stay inside the current issue.
- Run the tests above before opening the pull request.
- Keep secrets out of files, logs, and workflow JSON.

Don't:

- Change how a workflow behaves unless the issue asks for that.
- Put an API key, password, or token in a file.
- Add agent roles, shipping routines, or deploy steps to this guide.
- Weaken a test so it passes.
- Merge. Roxana merges.
