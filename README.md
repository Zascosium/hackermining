# HackerMining

> 20 years of Hacker News — a data investigation

**Live site:** https://zascosium.github.io/hackermining

Hacker News is the tech industry's water cooler. This project mines the full public dataset — 5.5M stories and 42M comments, 2006 to present — to find non-obvious patterns in the style of David Kriesel's SpiegelMining and BahnMining.

---

## Key findings

1. **Technology hype cycles are shockingly short** — most go from peak to background noise in under 4 years (NFT: peak 2021, irrelevant by 2024)
2. **ChatGPT was a 10× discontinuity** — the largest single-event spike in 18 years of data, dwarfing AlphaGo, GPT-3, and DALL-E combined
3. **Weekday mornings (US time) outperform** — weekend and late-night UTC posts score measurably lower across all years
4. **HN attention is extraordinarily unequal** — Gini coefficient 0.845, top 1% of stories capture 32.6% of all upvotes ever cast
5. **GitHub replaced personal blogs** as the dominant link target by 2015, and has widened its lead every year since
6. **AI content now dominates the viral tier** — AI-related stories (LLMs, generative AI, OpenAI, Anthropic, Copilot, Stable Diffusion, etc.) account for a far larger share of high-scoring content post-2022; the volume of breakout AI stories has exploded even though median AI story scores no higher than average
7. **A small network of ~50 power users** drives a disproportionate share of front-page content — HN curation is less random than it appears

---

## Structure

```
hackermining/
├── notebooks/
│   ├── 01_data_acquisition.ipynb   # BigQuery → local parquet (run once)
│   ├── 02_hype_cycles.ipynb        # Technology hype cycle heatmap
│   ├── 03_front_page_anatomy.ipynb # What actually predicts a viral post
│   ├── 04_domain_dominance.ipynb   # Who owns each era of HN
│   ├── 05_ai_discourse.ipynb       # AI/LLM timeline and viral share
│   ├── 06_community_behavior.ipynb # Gini, power users, post types
│   └── 07_key_findings.ipynb       # Summary with all headline charts
├── src/
│   ├── loader.py   # BigQuery + DuckDB helpers
│   ├── nlp.py      # Keyword tracking, VADER sentiment, domain extraction
│   └── viz.py      # Consistent chart style across all notebooks
├── _quarto.yml     # Quarto static site config
└── index.qmd       # Landing page
```

---

## Reproducing the analysis

### Option A — View only (no BigQuery needed)

The notebooks are saved with outputs. Clone the repo and build the site directly:

```bash
pip install -e .
quarto render
quarto preview   # opens the site locally
```

### Option B — Re-run from scratch

Requires a Google Cloud account with BigQuery API enabled (free tier covers this project).

```bash
# 1. Install dependencies
pip install -e .

# 2. Authenticate with Google Cloud
brew install google-cloud-sdk   # macOS; see cloud.google.com/sdk for others
gcloud init
gcloud auth application-default login

# 3. Configure project
cp .env.example .env
# Set GCP_PROJECT_ID in .env

# 4. Download data (one-time, ~10–15 min, uses ~10 GB BigQuery free quota)
# Open notebook 01 in Jupyter and run all cells:
jupyter lab notebooks/01_data_acquisition.ipynb

# 5. Run analysis notebooks 02–06 in Jupyter, then save with outputs

# 6. Build and publish
quarto render
quarto publish gh-pages
```

---

## Tech stack

| Tool | Purpose |
|---|---|
| Google BigQuery | Source: 5.5M stories + 42M comments, 2006–present |
| DuckDB | Fast SQL over local parquet — no database server needed |
| pandas | Data manipulation and aggregation |
| matplotlib / seaborn | Charts (static, publication-style) |
| VADER | Title sentiment scoring |
| Quarto | Converts notebooks to a static website |
| GitHub Pages | Free hosting for the rendered site |
