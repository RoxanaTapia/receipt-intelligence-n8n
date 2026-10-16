# n8n Docker Setup

Self-hosted n8n for local development in the Receipt Intelligence System.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose v2)
- A terminal and a web browser

## Quick start

1. **Copy environment variables** (never commit `.env`):

   ```bash
   cp .env.example .env
   ```

2. **Set a strong password** in `.env`:

   ```bash
   N8N_BASIC_AUTH_PASSWORD=your-strong-password-here
   ```

3. **Start n8n**:

   ```bash
   docker compose up -d
   ```

4. **Open the UI**: [http://localhost:5678](http://localhost:5678)

   Log in with the credentials from `.env` (`N8N_BASIC_AUTH_USER` / `N8N_BASIC_AUTH_PASSWORD`).

## Verify it works

```bash
docker compose ps
docker compose logs -f n8n
```

You should see the n8n container running and logs showing the editor is ready.

Stop n8n when you are done:

```bash
docker compose down
```

Data persists in the `n8n_data` Docker volume across restarts.

## Environment variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `N8N_HOST` | Hostname n8n uses for URLs | `localhost` |
| `N8N_PORT` | Port exposed on your machine | `5678` |
| `N8N_PROTOCOL` | `http` or `https` | `http` |
| `WEBHOOK_URL` | Base URL for webhook triggers | `http://localhost:5678/` |
| `GENERIC_TIMEZONE` | Timezone for schedules and dates | `Europe/Berlin` |
| `N8N_BASIC_AUTH_ACTIVE` | Require login before using the UI | `true` |
| `N8N_BASIC_AUTH_USER` | Basic auth username | `admin` |
| `N8N_BASIC_AUTH_PASSWORD` | Basic auth password (**required**) | — |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude nodes | — |
| `API_BASE_URL` | Sibling FastAPI base URL (analytics/Q&A HTTP; Module 5+) | `http://host.docker.internal:8000` |

See `.env.example` for a copy-paste template.

## n8n ↔ API integration contract

📌 **Demo recipe (start both apps, sample PDF → API in n8n):** [integration.md](integration.md).

Local integration uses **two channels** with different jobs:

| Channel | Role | Today |
|---------|------|-------|
| **Shared disk** | n8n **writes** categorized JSON; the API **reads** the same folder | ✅ In use |
| **HTTP** (`API_BASE_URL`) | After persist: coverage smoke, analytics summary, then fixed demo Q&A (`POST /questions`) | ✅ Wired in [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) |

📌 We do **not** POST receipt JSON to the API for ingest. Files on disk are the handoff. The demo Q&A step posts a **fixed** question only — not free-form chat.

### Shared disk (`data/receipts/` ↔ `RECEIPT_DATA_PATH`)

Expected sibling layout:

```text
receipt-intelligence-system/
├── receipt-intelligence-n8n/   # this repo — writes data/receipts/
└── receipt-intelligence-api/   # FastAPI — reads via RECEIPT_DATA_PATH
```

| Side | Path / variable |
|------|-----------------|
| This repo (host) | [`data/receipts/`](../data/README.md) |
| This repo (container Write File) | `/home/node/.n8n-files/receipts/` (bind-mounted) |
| API | `RECEIPT_DATA_PATH` — default `../receipt-intelligence-n8n/data/receipts` in the [API `.env.example`](https://github.com/RoxanaTapia/receipt-intelligence-api/blob/main/.env.example) |

API setup and loader details: [analytics guide](https://github.com/RoxanaTapia/receipt-intelligence-api/blob/main/docs/analytics.md) in the sibling repo.

### `API_BASE_URL` reachability

| Caller | Typical value |
|--------|----------------|
| n8n **inside** Docker (macOS Docker Desktop) | `http://host.docker.internal:8000` (default in `.env.example`) |
| Browser or terminal on the **host** | `http://localhost:8000` |

`localhost` inside the container means the container itself — not your Mac. Use `host.docker.internal` when HTTP Request nodes call the API from n8n.

Compose sets `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` so expressions like `={{ $env.API_BASE_URL }}` work in those nodes. Recreate the container after changing compose (`docker compose down && docker compose up -d`).

### Post-persist coverage smoke

Thinnest proof the API can **see** what n8n just wrote:

```text
sample PDF → ingest → Write File — Persist Receipt JSON
  → GET /health → IF — API Health OK
  → GET /analytics/receipts → IF — API Receipts OK
  → Code — Show Coverage Smoke → IF — Coverage Present
```

| Step | What to check |
|------|----------------|
| API running | Sibling FastAPI with `RECEIPT_DATA_PATH` → this repo’s `data/receipts/` |
| Import workflow | [`workflows/receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) |
| Execute | Manual Trigger with a [sample PDF](../samples/README.md) |
| Coverage | Open **`Code — Show Coverage Smoke`**: `api_status` is `ok`, `persistedInCoverage` is `true`, and `persistedFilename` appears in `loaded_files` |

### Post-persist analytics summary

After coverage is present, the happy path asks the API for spending context in the same run:

```text
IF — Coverage Present
  → GET /analytics/summary?preset=last_N_days&n_days=90 → IF — API Summary OK
  → Code — Show Analytics Summary
```

| Step | What to check |
|------|---------------|
| Summary call | **`HTTP Request — GET Analytics Summary`** uses `preset=last_N_days` and `n_days=90` (explicit time range; covers May sample dates) |
| Visible output | Open **`Code — Show Analytics Summary`**: named fields include `period_label`, `total_spend`, `top_categories`, `by_category`, `summary_facts` |

Empty periods still return **200** with `total_spend: 0` — that is success, not an error (files exist; the time window just has no spend).

### Post-persist demo Q&A

After the analytics summary, the happy path asks one **fixed** demo question so a natural-language answer appears in the same run (portfolio demo — not a chat UI):

```text
Code — Show Analytics Summary
  → POST /questions  { "question": "How much did I spend on food last month?" }
  → IF — API Questions OK → Code — Show Demo Q&A Answer
```

| Step | What to check |
|------|----------------|
| Demo call | **`HTTP Request — POST Demo Questions`** uses that fixed body (not user input) |
| Visible output | Open **`Code — Show Demo Q&A Answer`**: `demo` is `true`, `answer` is set (or `meta` shows a refusal), plus routing fields (`intent`, `categories`, `time_range`) |
| API Anthropic | Sibling FastAPI needs `ANTHROPIC_API_KEY` for `POST /questions` — `/health` and `/analytics/*` can succeed without it; Q&A cannot. See the [API Q&A setup](https://github.com/RoxanaTapia/receipt-intelligence-api/blob/main/docs/question-answering.md#setup-and-curl) |

### Post-persist failure modes

HTTP Request nodes use a **5s timeout**, **continue-on-fail**, and **bounded retries** (`retryOnFail`: up to **3** attempts with **1s** between tries — 1 initial + 2 retries). After retries are exhausted, failures still land on the terminals below. Persist is never undone when an API call fails.

| Situation | Where it lands | What you see |
|-----------|----------------|--------------|
| Connection refused / timeout / 5xx after retries exhausted (any post-persist HTTP step) | **`Set — API Error`** | `valid: false`, `stage: "api"`, `errors` with the failure message |
| API up but empty store / persisted file missing from coverage | **`Set — Empty Coverage`** | `valid: false`, `stage: "coverage"` — stops before summary/Q&A (no fake analytics success; **not** retried as a transport blip) |
| Missing API `ANTHROPIC_API_KEY` on demo Q&A | **`Set — API Error`** | Same API error branch after `POST /questions` |

📌 A successful write under `data/receipts/` stays on disk in all of these cases — including while HTTP retries run and after a final API error.

Full local full-stack runbook: [integration.md](integration.md).

## Security notes

- **Do not commit `.env`** — it is listed in `.gitignore`.
- **Use basic auth** for local self-hosted n8n so the editor is not open to anyone on your network.
- **Change the default password** before first run.
- Workflows and credentials are stored in the `n8n_data` volume, not in git.

## Workflows in git

Workflow JSON files live in [`workflows/`](../workflows/). They are the version-controlled source of truth; your running n8n instance stores its own copy in the `n8n_data` Docker volume.

### Import a workflow

1. Open [http://localhost:5678](http://localhost:5678) and log in.
2. Go to **Workflows** (left sidebar) → **Add workflow** → **Import from file** (or use the **⋯** menu → **Import from file**).
3. Select a JSON file from `workflows/` — start with [`hello-world.json`](../workflows/hello-world.json).
4. Click **Execute workflow** and confirm the output in the **Set Test Payload** node:

   ```json
   {
     "message": "Hello from Receipt Intelligence!",
     "project": "receipt-intelligence-n8n"
   }
   ```

### Export a workflow

After editing a workflow in the UI: **⋯** → **Download** (or **Export**). Save the JSON under `workflows/` and commit it so the team can import the same version.

### Run the PDF ingest workflow

[`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) runs the full ingest path: PDF → Claude extraction → categorization → validated JSON on disk → post-persist API smoke (coverage, analytics summary, demo Q&A). Node walkthroughs: [pdf-extraction.md](pdf-extraction.md) → [categorization.md](categorization.md). Full-stack demo: [integration.md](integration.md).

1. Set `ANTHROPIC_API_KEY` in `.env` and restart n8n if you have not already.
2. Import the workflow (see **Import a workflow** above).
3. Confirm sample PDFs are mounted read-only at `/home/node/.n8n-files/samples` (Compose maps `./samples/receipts`). No `docker cp` for the demo sample.
4. **Operator (Manual Trigger):** open the workflow → **Execute workflow**. Resolves the default allowlisted sample (`03-small`).
5. Confirm a hash-named JSON file appears in `data/receipts/` on your host (see [data/README.md](../data/README.md)).

To try another allowlisted sample via webhook, pass `{ "sample": "<id>" }` (see **Demo sample webhook** below). Operators can also change the default by editing **Code — Resolve Sample Path**.

### Demo sample webhook

📌 **Visitor vs operator:** the portfolio demo UX calls this webhook over **Compose service DNS** after the visitor uploads a known sample. Operators keep using **Manual Trigger** in the n8n UI. n8n is the engine, not the product UI.

| Item | Value |
|------|--------|
| Caller | Demo UX / another Compose service → `http://n8n:5678/webhook/receipt-demo-ingest` (not the browser → a public webhook) |
| Host smoke (optional) | `http://localhost:5678/webhook/receipt-demo-ingest` |
| Method | `POST` |
| Body | `{ "sample": "03-small" }` or empty / omit `sample` → default `03-small`. Portfolio UX uses `{ "sample": "sample-supermarket-receipt" }`. `{ "sample": "05-demo-basket" }` remains allowed so current deploys keep working. |
| Binary | n8n **reads** the bind-mounted allowlisted PDF after validating the id (UX does not need to forward bytes to n8n) |
| Allowlist | `03-small`, `01-food-homedeco`, `02-vegetables-weighted`, `04-article-discount`, `05-demo-basket`, `sample-supermarket-receipt` → `/home/node/.n8n-files/samples/<id>.pdf` |
| Workflow | Must be **Active** for production webhook URLs (`/webhook/...`). Inactive workflows only serve `/webhook-test/...` from the editor |
| Auth / network | Intended for **internal** Compose traffic. Do not expose this path as an open internet upload API — the demo edge gate owns visitor access |

**Success** — HTTP response is sent **after** **Write File — Persist Receipt JSON**, then post-persist coverage / summary / Q&A may continue without blocking the client:

```json
{
  "ok": true,
  "persistedFilename": "2025-05-12_rewe-musterstadt_a1b2c3d4.json",
  "merchant": "REWE Musterstadt",
  "date": "2025-05-12",
  "total": 12.34
}
```

**Unknown sample** — clear client error (HTTP 400):

```json
{
  "ok": false,
  "error": "unknown_sample",
  "message": "Unknown sample id 'nope'. Allowed: 03-small, …",
  "sample": "nope"
}
```

**Pipeline failure** (extract / categorize after retries) — HTTP 422 with `stage` and `errors`. Disk handoff is unchanged: we still do **not** POST receipt JSON to the API for ingest.

```json
{
  "ok": false,
  "error": "pipeline_failed",
  "stage": "parse",
  "errors": ["Claude did not return valid JSON after 3 attempts"]
}
```

```bash
# From another Compose service (demo UX):
curl -sS -X POST http://n8n:5678/webhook/receipt-demo-ingest \
  -H 'Content-Type: application/json' \
  -d '{"sample":"03-small"}'

# Unknown id (expect ok: false):
curl -sS -X POST http://n8n:5678/webhook/receipt-demo-ingest \
  -H 'Content-Type: application/json' \
  -d '{"sample":"not-a-sample"}'
```

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| Port 5678 already in use | Change `N8N_PORT` in `.env` (e.g. `5679`) and update `WEBHOOK_URL` to match |
| `N8N_BASIC_AUTH_PASSWORD` error on start | Create `.env` from `.env.example` and set a password |
| Container exits immediately | Run `docker compose logs n8n` and check for env or port conflicts |
| Fresh start (wipe workflows) | `docker compose down -v` (**deletes** the `n8n_data` volume) |
| Read Binary File: "Access to the file is not allowed" | n8n only allows paths under `/home/node/.n8n-files`. Confirm Compose mounts `samples/receipts` → `/home/node/.n8n-files/samples` and recreate the container |
| Webhook returns 404 | Workflow must be **Active** for `/webhook/...` (editor test URL is `/webhook-test/...`) |
| Webhook hangs with no body | Confirm **Webhook — Demo Sample Ingest** uses **Respond to Webhook** (`responseMode: responseNode`) and failure branches also respond |

## Related docs

| Doc | Role |
|-----|------|
| [Docs index](README.md) | Reading order |
| [integration.md](integration.md) | Full-stack demo recipe |
| [pdf-extraction.md](pdf-extraction.md) | Extraction pipeline |
| [categorization.md](categorization.md) | Categorization and persist |
| [data/README.md](../data/README.md) | Receipt JSON store |
| [samples/README.md](../samples/README.md) | Sample PDFs |
| [n8n-claude-standards.md](n8n-claude-standards.md) | Claude vs deterministic nodes |
