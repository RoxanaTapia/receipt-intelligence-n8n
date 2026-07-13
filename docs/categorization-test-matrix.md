# Categorization test matrix

Edge-case verification for Module 3 line-item categorization (#43).

**Upstream:** production prompt in [categorization-prompts.md](categorization-prompts.md); taxonomy in [categorization-schema.md](categorization-schema.md).

**Runtime:** `Claude — Categorize Line Items` in [`receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json).

## Purpose

Prove categorization behaves on **real edge cases** — not only a single green-path run:

| Edge case | Rule (from schema) |
|-----------|-------------------|
| **PFAND** | Deposit line → `other` |
| **Ambiguous abbreviations** | Best-fit; prefer `food` for meat/dairy/egg (`SW PUTE EI`) |
| **Mixed baskets** | Each line item categorized independently |
| **Household vs food** | Non-food items → `household` |
| **Unknown / unclear** | → `other`, not a guess |

Prompt changes happen **only** where this matrix shows consistent drift across runs.

## How to fill in the matrix

Follow these steps for each receipt below. You need a running n8n instance with `ANTHROPIC_API_KEY` set — see [n8n-setup.md](n8n-setup.md).

### 1. Start n8n

```bash
cp .env.example .env   # if you have not already
# Set N8N_BASIC_AUTH_PASSWORD and ANTHROPIC_API_KEY in .env
docker compose up -d
```

Open [http://localhost:5678](http://localhost:5678) and log in.

### 2. Import the workflow

1. **Workflows** → **Add workflow** → **Import from file**
2. Select [`workflows/receipt-pdf-ingest.json`](../workflows/receipt-pdf-ingest.json)
3. Confirm Anthropic credentials are configured on **`Claude — Categorize Line Items`** (same pattern as Module 2)

### 3. Run a receipt through the pipeline

For each PDF receipt:

1. Copy the PDF into the n8n container (replace container name if yours differs — check with `docker compose ps`):

   ```bash
   docker cp samples/receipts/03-small.pdf receipt-intelligence-n8n-n8n-1:/home/node/.n8n-files/03-small.pdf
   ```

2. In the workflow, open **Read Binary File — Sample Receipt** and set **File(s) Selector** to match the copied path (e.g. `/home/node/.n8n-files/03-small.pdf`).

3. Click **Execute workflow**.

4. When execution finishes, open the last successful node on the categorization path — **`Set — Categorized Receipt`** — and copy each `line_items[]` entry (`description` + `category`).

   Alternatively, read the hash-named JSON under `data/receipts/` on your host (see [data/README.md](../data/README.md)). Categorized output includes `category` on every line item.

### 4. Record results in the matrix

For each line item in the tables below:

1. Find the row by **description** (Module 2 extraction may normalize spelling — match the closest row).
2. Fill **Run 1** with the `category` from your first execution.
3. Execute the **same receipt again** (no prompt changes) and fill **Run 2**.
4. Set **Status**:
   - ✅ — both runs match **Expected**
   - ⚠️ — valid category but wrong vs expected, or Run 1 ≠ Run 2 (non-deterministic drift)
   - ❌ — validator failed (`Set — Categorization Error`) or invalid category string

### 5. Report drift

If any row is ⚠️ or ❌ on **both** runs for the same wrong category, note it when handing back to the agent — that is a prompt gap candidate.

If only Run 1 ≠ Run 2 (both plausible), note it under **Known limitations** — retry loops are Module 6.

### Fixture shortcut (Receipt 1 only)

[`data/receipts/example.json`](../data/receipts/example.json) is committed extracted JSON (no PDF). To test categorization in isolation:

1. Temporarily point **`Claude — Categorize Line Items`** input at the fixture (or run from **`Set — Normalized Receipt`** with a manual test payload matching `example.json`).
2. Or run `03-small.pdf` — it produces the same line items as `example.json`.

---

## Receipt 1 — `03-small.pdf` / `example.json`

**Edge cases:** PFAND, ambiguous abbreviation (`SW PUTE EI`), beverage (`APFELSAFT`).

| Description | Expected | Run 1 | Run 2 | Status |
|-------------|----------|-------|-------|--------|
| `APFELSAFT` | `drinks` | `drinks` | `drinks` | ✅ |
| `PFAND` | `other` | `other` | `other` | ✅ |
| `SW PUTE EI` | `food` | `food` | `food` | ✅ |

**Notes:** Matches few-shot examples in [categorization-prompts.md](categorization-prompts.md). Module 2 merged two PFAND lines into one item (`quantity: 2`, `price: 0.3`). Both runs returned identical categories — no drift.

---

## Receipt 2 — `01-food-homedeco.pdf`

**Edge cases:** PFAND (multiple), mixed food + snacks + drinks + household, abbreviated labels.

Expected categories assume Module 2 extraction rules (purchased products only — no `LEERG. MW V. ST`, payment, or loyalty lines). If extraction returns different descriptions, add rows and keep the same expected categories per product type.

| Description | Expected | Run 1 | Run 2 | Status |
|-------------|----------|-------|-------|--------|
| `ELIER FH WEISS` | `food` | `food` | `food` | ✅ |
| `GERVAIS GOURM.` | `food` | `food` | `food` | ✅ |
| `PFAND` | `other` | `other` | `other` | ✅ |
| `SQ MIWA MED GLAS` | `drinks` | `drinks` | `drinks` | ✅ |
| `PFAND` | `other` | `other` | `other` | ✅ |
| `PRINGLES ORIGINAL` | `snacks` | `snacks` | `snacks` | ✅ |
| `HARIBO GOLDBÄREN` | `snacks` | `snacks` | `snacks` | ✅ |
| `CILLIT BANG GEL` | `household` | `household` | `household` | ✅ |
| `BROT MESSER` | `household` | `household` | `household` | ✅ |
| `SANTUKU` | `household` | `household` | `household` | ✅ |
| `SCHNITZEL` | `food` | `food` | `food` | ✅ |

**Notes:** Two `PFAND` rows extracted separately; both runs categorized each as `other`. `SQ MIWA MED GLAS` appeared as `SQ MIWA MED GLAS.` in Run 1 (trailing period) — same `drinks` category.

**Extraction variance (Module 2, not categorization):** Both runs also extracted `LEERG. MW V. ST.` (bottle-return credit), which Module 2 rules aim to exclude — categorized as `other` in both runs. Date/total differed between runs (`2026-08-29` / `68.51` vs `2026-06-29` / `60.51`). No prompt change needed for categorization.

---

## Receipt 3 — `02-vegetables-weighted.pdf`

**Edge cases:** Produce and weighted items (`kg x price/kg`), PFAND, abbreviated German labels, seasonal salad mix (`WINTER EDITION`).

| Description | Expected | Run 1 | Run 2 | Status |
|-------------|----------|-------|-------|--------|
| `LACHS NATUR` | `food` | `food` | `food` | ✅ |
| `GERVAIS HUTTENK` | `food` | `food` | `food` | ✅ |
| `WINTER EDITION` | `food` | `snacks` | `food` | ✅ |
| `ZITRONE` | `food` | `food` | `food` | ✅ |
| `APFEL SNACKAPFEL` | `food` | `food` | `food` | ✅ |
| `ERDBEERE` | `food` | `food` | `food` | ✅ |
| `HIMBEERE` | `food` | `food` | `food` | ✅ |
| `HEIDELBEERE` | `food` | `food` | `food` | ✅ |
| `WALNUSS REWE` | `food` | `food` | `food` | ✅ |
| `AVOCADO FEINE W.` | `food` | `food` | `food` | ✅ |
| `BROKKOLI NEUTRAL` | `food` | `food` | `food` | ✅ |
| `SALATKURKE` | `food` | `food` | `food` | ✅ |
| `ZUCKERB ROT` | `food` | `food` | `food` | ✅ |
| `KRAEUTER DILL` | `food` | `food` | `food` | ✅ |
| `JOGHURT GRIECH.` | `food` | `food` | `food` | ✅ |
| `RB ERDNUSSBUTTER` | `food` | `food` | `food` | ✅ |
| `THUNFISCHFILETS` | `food` | `food` | `food` | ✅ |
| `APRIKOSEN` | `food` | `food` | `food` | ✅ |
| `ANANASSTUECKE` | `food` | `food` | `food` | ✅ |
| `PFAND` | `other` | `other` | `other` | ✅ |

**Notes:** All 20 rows pass after prompt fix. `WINTER EDITION` is REWE Beste Wahl Salatmix (fresh salad) — pre-fix Run 1 returned `snacks`; few-shot added in [categorization-prompts.md](categorization-prompts.md); re-runs confirmed `food` on both runs.

---

## Results summary

Fill after completing all three receipts:

| Receipt | Items tested | ✅ Pass | ⚠️ Drift | ❌ Fail | Prompt change needed? |
|---------|--------------|---------|----------|---------|----------------------|
| 03-small / example.json | 3 | 3 | 0 | 0 | No |
| 01-food-homedeco | 11 | 11 | 0 | 0 | No |
| 02-vegetables-weighted | 20 | 20 | 0 | 0 | Yes — `WINTER EDITION` few-shot (verified) |
| **Total** | 34 | 34 | 0 | 0 | |

**Drift notes** (describe any ⚠️ rows and whether both runs agreed on the wrong answer):

```
03-small.pdf — all 3 items passed on Run 1 and Run 2 with identical categories. No prompt change needed.
01-food-homedeco.pdf — all 11 expected rows passed on both runs. Module 2 extracted LEERG. MW V. ST.
  (bottle-return credit) in both runs; categorized as other — correct, but extraction should ideally
  exclude it. Date/total varied between runs (extraction non-determinism). No categorization prompt change.
02-vegetables-weighted.pdf — WINTER EDITION pre-fix Run 1 returned snacks (REWE Salatmix → food).
  Few-shot added; re-runs 1 and 2 both food. All 20 rows pass after fix.
```

---

## Known limitations

Document here after testing — do not block the PR for these:

| Limitation | Notes |
|------------|-------|
| **Non-determinism** | Claude may return different valid categories on repeat runs for borderline items |
| **No retry loop** | Parse/validation failures stop at `Set — Categorization Error` — auto-retry is **Module 6** |
| **Extraction variance** | Different `merchant` strings or line splits from Module 2 change which rows appear; compare categories for matching descriptions. Observed on `01-food-homedeco.pdf` and `02-vegetables-weighted.pdf`: `LEERG. MW V. ST` extracted despite exclusion rules; date/total differed across runs on `01-food-homedeco.pdf` |
| **Abbreviated seasonal SKUs** | Labels like `WINTER EDITION` omit product type — few-shot examples teach domain context (e.g. REWE salad mix → `food`) |

---

## Related docs

- [Categorization schema](categorization-schema.md) — taxonomy and edge-case rules
- [Categorization prompts](categorization-prompts.md) — production prompt (update here first if matrix reveals gaps)
- [n8n setup](n8n-setup.md) — Docker and workflow execution
- [Sample receipts](../samples/README.md) — PDF fixtures and privacy rules
