"""Data loading helpers: BigQuery → parquet, then DuckDB for local queries."""

from __future__ import annotations

import os
from pathlib import Path

import duckdb
import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"

STORIES_PARQUET = DATA_DIR / "hn_stories.parquet"
COMMENTS_PARQUET = DATA_DIR / "hn_comments.parquet"

# BigQuery SQL templates
_STORIES_QUERY = """
SELECT
    id,
    title,
    url,
    score,
    `by` AS author,
    time AS unix_time,
    TIMESTAMP_SECONDS(time) AS posted_at,
    descendants AS comment_count,
    type
FROM `bigquery-public-data.hacker_news.full`
WHERE type = 'story'
  AND title IS NOT NULL
  AND score IS NOT NULL
  AND time IS NOT NULL
ORDER BY time
"""

_COMMENTS_QUERY = """
SELECT
    id,
    parent,
    `by` AS author,
    time AS unix_time,
    TIMESTAMP_SECONDS(time) AS posted_at,
    LENGTH(text) AS text_length
FROM `bigquery-public-data.hacker_news.full`
WHERE type = 'comment'
  AND time IS NOT NULL
ORDER BY time
"""


def fetch_from_bigquery(project_id: str, force: bool = False) -> None:
    """Download stories and comments from BigQuery and save as parquet.

    Only runs if parquet files don't already exist (or force=True).
    Requires: gcloud auth application-default login, or GOOGLE_APPLICATION_CREDENTIALS set.
    """
    import google.cloud.bigquery as bq

    if STORIES_PARQUET.exists() and COMMENTS_PARQUET.exists() and not force:
        print("Parquet files already exist. Pass force=True to re-download.")
        return

    client = bq.Client(project=project_id)

    print("Fetching stories (~2–5 min)...")
    stories_df = client.query(_STORIES_QUERY).to_dataframe(progress_bar_type="tqdm")
    stories_df.to_parquet(STORIES_PARQUET, index=False)
    print(f"Saved {len(stories_df):,} stories → {STORIES_PARQUET}")

    print("Fetching comments (~5–10 min)...")
    comments_df = client.query(_COMMENTS_QUERY).to_dataframe(progress_bar_type="tqdm")
    comments_df.to_parquet(COMMENTS_PARQUET, index=False)
    print(f"Saved {len(comments_df):,} comments → {COMMENTS_PARQUET}")


def db() -> duckdb.DuckDBPyConnection:
    """Return a DuckDB connection with stories and comments registered as views."""
    con = duckdb.connect()
    if STORIES_PARQUET.exists():
        con.execute(f"CREATE VIEW stories AS SELECT * FROM read_parquet('{STORIES_PARQUET}')")
    if COMMENTS_PARQUET.exists():
        con.execute(f"CREATE VIEW comments AS SELECT * FROM read_parquet('{COMMENTS_PARQUET}')")
    return con


def stories_df() -> pd.DataFrame:
    """Load full stories parquet into a pandas DataFrame."""
    return pd.read_parquet(STORIES_PARQUET)
