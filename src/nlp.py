"""NLP utilities: keyword tracking, sentiment, URL domain extraction."""

from __future__ import annotations

import re
from urllib.parse import urlparse

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_vader = SentimentIntensityAnalyzer()

# Technology keyword groups for hype cycle tracking
TECH_KEYWORDS: dict[str, list[str]] = {
    # Languages
    "Python": ["python"],
    "Ruby": ["ruby", "ruby on rails", "rails"],
    "PHP": ["php"],
    "Go": [r"\bgo\b", "golang"],
    "Rust": [r"\brust\b", "rustlang"],
    "TypeScript": ["typescript"],
    "Scala": ["scala"],
    # Infrastructure & paradigms
    "Docker": ["docker", "container"],
    "Kubernetes": ["kubernetes", r"\bk8s\b"],
    "Serverless": ["serverless", "lambda function", "faas"],
    "Microservices": ["microservice"],
    "DevOps": ["devops"],
    # Cloud
    "AWS": [r"\baws\b", "amazon web services"],
    "Heroku": ["heroku"],
    # Crypto / Web3
    "Bitcoin": ["bitcoin", r"\bbtc\b"],
    "Blockchain": ["blockchain"],
    "NFT": [r"\bnft\b", "non-fungible"],
    "Web3": ["web3", "web 3"],
    # AI
    "Machine Learning": ["machine learning", r"\bml\b model"],
    "Deep Learning": ["deep learning", "neural network"],
    "GPT": [r"\bgpt\b", "gpt-2", "gpt-3", "gpt-4"],
    "ChatGPT": ["chatgpt"],
    "LLM": [r"\bllm\b", "large language model"],
    "Transformer": ["transformer model", "attention mechanism"],
    # Platforms / products
    "Twitter/X": ["twitter"],
    "Medium": ["medium.com"],
    "Substack": ["substack"],
}


def keyword_hits(title: str, patterns: list[str]) -> bool:
    """Return True if any pattern matches in a lowercased title."""
    title_lower = title.lower()
    return any(re.search(p, title_lower) for p in patterns)


def add_keyword_columns(df: pd.DataFrame, title_col: str = "title") -> pd.DataFrame:
    """Add a boolean column per keyword group to a stories DataFrame."""
    for name, patterns in TECH_KEYWORDS.items():
        col = f"kw_{name.lower().replace('/', '_').replace(' ', '_')}"
        df[col] = df[title_col].apply(lambda t: keyword_hits(str(t), patterns))
    return df


def sentiment_score(text: str) -> float:
    """Return VADER compound sentiment score in [-1, 1]."""
    return _vader.polarity_scores(text)["compound"]


def extract_domain(url: str | None) -> str:
    """Return registered domain (e.g. 'github.com') from a URL string."""
    if not url or not isinstance(url, str):
        return "self"
    try:
        host = urlparse(url).netloc.lower()
        # Strip www.
        host = re.sub(r"^www\.", "", host)
        return host or "self"
    except Exception:
        return "unknown"


def title_features(df: pd.DataFrame, title_col: str = "title") -> pd.DataFrame:
    """Add engineered title features used in front-page anatomy analysis."""
    titles = df[title_col].fillna("")
    df["title_len_chars"] = titles.str.len()
    df["title_len_words"] = titles.str.split().str.len()
    df["title_is_question"] = titles.str.strip().str.endswith("?")
    df["title_has_number"] = titles.str.contains(r"\b\d+\b", regex=True)
    df["title_sentiment"] = titles.apply(sentiment_score)
    return df
