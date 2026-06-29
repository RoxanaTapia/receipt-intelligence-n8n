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

See `.env.example` for a copy-paste template.

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

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| Port 5678 already in use | Change `N8N_PORT` in `.env` (e.g. `5679`) and update `WEBHOOK_URL` to match |
| `N8N_BASIC_AUTH_PASSWORD` error on start | Create `.env` from `.env.example` and set a password |
| Container exits immediately | Run `docker compose logs n8n` and check for env or port conflicts |
| Fresh start (wipe workflows) | `docker compose down -v` (**deletes** the `n8n_data` volume) |
