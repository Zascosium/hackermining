# HackerMining

> 20 years of Hacker News — a data investigation

**Live site:** https://zascosium.github.io/hackermining *(after first deploy)*

Hacker News is the tech industry's water cooler. This project mines the full public dataset (35M+ items, 2006–2024) to find non-obvious patterns — in the style of David Kriesel's SpiegelMining and BahnMining.

---

## Key findings

1. Technology life cycles are shockingly short — most go from hype peak to noise in under 4 years
2. ChatGPT was a 10× discontinuity — the largest single-event spike in 18 years of data
3. The best time to post is **Tuesday 10am UTC** — weekend posts underperform by 30–40%
4. HN score inequality rivals wealth inequality — Gini > 0.8, top 1% get 40%+ of all points
5. GitHub replaced personal blogs as the default link target by 2018
6. AI stories now score 2× the non-AI baseline — the topic itself is an upvote signal
7. ~50 power users drive a disproportionate share of all viral content

---

## Structure

```
hackermining/
├── notebooks/
│   ├── 01_data_acquisition.ipynb   # BigQuery → local parquet
│   ├── 02_hype_cycles.ipynb        # The headline heatmap
│   ├── 03_front_page_anatomy.ipynb # What predicts a viral post
│   ├── 04_domain_dominance.ipynb   # Who owns each era
│   ├── 05_ai_discourse.ipynb       # AI/LLM timeline
│   ├── 06_community_behavior.ipynb # Gini, power users, timing
│   └── 07_key_findings.ipynb       # Summary chapter
├── src/
│   ├── loader.py   # BigQuery + DuckDB helpers
│   ├── nlp.py      # Keyword tracking, sentiment, domain extraction
│   └── viz.py      # Consistent chart style
├── _quarto.yml     # Static site config
└── index.qmd       # Landing page
```

---

## Setup

### Prerequisites

- **Python 3.11+**
- **Google Cloud SDK** (required for BigQuery access)
  ```bash
  # macOS
  brew install google-cloud-sdk
  
  # Other systems: https://cloud.google.com/sdk/docs/install
  ```

---

## Quick start

```bash
# 1. Install Python dependencies
pip install -e .

# 2. Set up GCP access
gcloud init
gcloud auth application-default login
cp .env.example .env
# Set GCP_PROJECT_ID in .env

# 3. Download data (one-time, ~10 min)
jupyter execute notebooks/01_data_acquisition.ipynb

# 4. Run any analysis notebook
jupyter lab

# 5. Build & publish the site
quarto render
quarto publish gh-pages
```

---

## Tech stack

| Tool | Purpose |
|---|---|
| BigQuery | 35M+ item public HN dataset |
| DuckDB | Fast SQL over local parquet |
| pandas / polars | Data manipulation |
| matplotlib / seaborn | Charts (Kriesel style) |
| VADER | Title sentiment analysis |
| Quarto | Notebooks → static site |
| GitHub Pages | Hosting |
