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

Local integration uses **two channels** with different jobs:

| Channel | Role | Today |
|---------|------|-------|
| **Shared disk** | n8n **writes** categorized JSON; the API **reads** the same folder | ✅ In use |
| **HTTP** (`API_BASE_URL`) | After persist: coverage smoke (`/health` + `/analytics/receipts`), then spending summary (`/analytics/summary`) | ✅ Wired in [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) |

📌 We do **not** POST receipt JSON to the API for ingest. Files on disk are the handoff. Demo Q&A HTTP (`POST /questions`) is a follow-up Module 5 Integration issue.

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
  → GET /health
  → GET /analytics/receipts
  → Code — Show Coverage Smoke
```

| Step | What to check |
|------|----------------|
| API running | Sibling FastAPI with `RECEIPT_DATA_PATH` → this repo’s `data/receipts/` |
| Import workflow | [`workflows/receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) |
| Execute | Manual Trigger with a [sample PDF](../samples/README.md) |
| Coverage | Open **`Code — Show Coverage Smoke`**: `api_status` is `ok`, `persistedInCoverage` is `true`, and `persistedFilename` appears in `loaded_files` |

If the API is down, the HTTP Request node fails the run (visible red) — graceful branching is a later issue.

### Post-persist analytics summary

After the coverage smoke, the happy path asks the API for spending context in the same run:

```text
Code — Show Coverage Smoke
  → GET /analytics/summary?preset=last_month
  → Code — Show Analytics Summary
```

| Step | What to check |
|------|---------------|
| Summary call | **`HTTP Request — GET Analytics Summary`** uses `preset=last_month` (explicit time range) |
| Visible output | Open **`Code — Show Analytics Summary`**: named fields include `period_label`, `total_spend`, `top_categories`, `by_category`, `summary_facts` |

Empty periods still return **200** with `total_spend: 0` — that is success, not an error. Deeper failure modes (API down, empty-data UX) are tracked separately.

Full local full-stack runbook: tracked in a follow-up issue (#71).

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

[`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json) runs the full Module 2 pipeline: PDF → Claude extraction → validation → JSON on disk. See [pdf-extraction.md](pdf-extraction.md) for the node walkthrough.

1. Set `ANTHROPIC_API_KEY` in `.env` and restart n8n if you have not already.
2. Import the workflow (see **Import a workflow** above).
3. Copy a sample PDF into n8n’s allowed files directory (Docker only reads under `/home/node/.n8n-files`):

   ```bash
   docker cp samples/receipts/03-small.pdf receipt-intelligence-n8n-n8n-1:/home/node/.n8n-files/03-small.pdf
   ```

   Run from the repo root. Replace the container name if yours differs (`docker compose ps`).

4. Open the workflow → **Execute workflow**.
5. Confirm a hash-named JSON file appears in `data/receipts/` on your host (see [data/README.md](../data/README.md)).

To try another sample, copy it the same way and update the path in **Read Binary File — Sample Receipt**, or re-export the workflow with a new path.

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| Port 5678 already in use | Change `N8N_PORT` in `.env` (e.g. `5679`) and update `WEBHOOK_URL` to match |
| `N8N_BASIC_AUTH_PASSWORD` error on start | Create `.env` from `.env.example` and set a password |
| Container exits immediately | Run `docker compose logs n8n` and check for env or port conflicts |
| Fresh start (wipe workflows) | `docker compose down -v` (**deletes** the `n8n_data` volume) |
| Read Binary File: "Access to the file is not allowed" | n8n only allows paths under `/home/node/.n8n-files`. Copy the PDF there with `docker cp` (see **Run the PDF ingest workflow**) |
