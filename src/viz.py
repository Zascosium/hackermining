"""Reusable chart helpers — consistent style across all notebooks."""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

# ── Style ─────────────────────────────────────────────────────────────────────

PALETTE = "YlOrRd"
BG = "#fafafa"
FG = "#1a1a1a"

def set_style() -> None:
    sns.set_theme(style="whitegrid", font_scale=1.15)
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "axes.edgecolor": "#cccccc",
        "text.color": FG,
        "axes.labelcolor": FG,
        "xtick.color": FG,
        "ytick.color": FG,
        "grid.color": "#e0e0e0",
        "font.family": "sans-serif",
    })


# ── Chart functions ────────────────────────────────────────────────────────────

def hype_heatmap(
    pivot: pd.DataFrame,
    title: str = "Technology Hype Cycles on Hacker News",
    figsize: tuple[int, int] = (16, 10),
) -> plt.Figure:
    """Heatmap of normalized keyword frequency: years × technologies."""
    set_style()
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        pivot,
        ax=ax,
        cmap=PALETTE,
        linewidths=0.3,
        linecolor="#e8e8e8",
        cbar_kws={"label": "Normalized mention frequency", "shrink": 0.6},
    )
    ax.set_title(title, fontsize=16, fontweight="bold", pad=14)
    ax.set_xlabel("Year")
    ax.set_ylabel("")
    plt.tight_layout()
    return fig


def time_series(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str = "",
    ylabel: str = "",
    figsize: tuple[int, int] = (14, 5),
) -> plt.Figure:
    """Line chart for one or more series over time."""
    set_style()
    fig, ax = plt.subplots(figsize=figsize)
    ys = [y] if isinstance(y, str) else y
    for col in ys:
        ax.plot(df[x], df[col], linewidth=2, label=col)
    if len(ys) > 1:
        ax.legend()
    ax.set_title(title, fontsize=15, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout()
    return fig


def bar_chart(
    labels: list[str],
    values: list[float],
    title: str = "",
    xlabel: str = "",
    color: str = "#e8604c",
    figsize: tuple[int, int] = (10, 6),
    horizontal: bool = True,
) -> plt.Figure:
    """Simple bar chart."""
    set_style()
    fig, ax = plt.subplots(figsize=figsize)
    if horizontal:
        ax.barh(labels, values, color=color, edgecolor="white")
        ax.set_xlabel(xlabel)
        ax.invert_yaxis()
    else:
        ax.bar(labels, values, color=color, edgecolor="white")
        ax.set_ylabel(xlabel)
        plt.xticks(rotation=45, ha="right")
    ax.set_title(title, fontsize=15, fontweight="bold")
    plt.tight_layout()
    return fig


def heatmap_2d(
    data: pd.DataFrame,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    fmt: str = ".0f",
    figsize: tuple[int, int] = (14, 5),
) -> plt.Figure:
    """Generic 2-D heatmap (e.g. hour-of-day × day-of-week)."""
    set_style()
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(data, ax=ax, cmap=PALETTE, fmt=fmt, linewidths=0.4, linecolor="#ececec")
    ax.set_title(title, fontsize=15, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return fig


def save(fig: plt.Figure, path: str, dpi: int = 150) -> None:
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
