"""Yahoo Finance collection logic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class YahooDataset:
    prices: pd.DataFrame
    volumes: pd.DataFrame
    returns: pd.DataFrame


def collect_daily_market_data(
    symbols: list[str],
    start: str,
    end: str | None = None,
) -> YahooDataset:
    """Download daily adjusted price and volume data for a symbol list."""
    if not symbols:
        raise ValueError("At least one symbol is required.")

    raw = yf.download(
        tickers=symbols,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )

    if raw.empty:
        raise RuntimeError("Yahoo Finance returned no data for the requested universe.")

    prices = _select_field(raw, "Close")
    volumes = _select_field(raw, "Volume")
    returns = prices.pct_change(fill_method=None)

    return YahooDataset(
        prices=_clean_frame(prices),
        volumes=_clean_frame(volumes),
        returns=_clean_frame(returns),
    )


def write_dataset(dataset: YahooDataset, output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "prices_daily": output_dir / "prices_daily.csv",
        "volumes_daily": output_dir / "volumes_daily.csv",
        "returns_daily": output_dir / "returns_daily.csv",
    }

    dataset.prices.to_csv(paths["prices_daily"], index_label="date")
    dataset.volumes.to_csv(paths["volumes_daily"], index_label="date")
    dataset.returns.to_csv(paths["returns_daily"], index_label="date")

    return {name: str(path) for name, path in paths.items()}


def _select_field(raw: pd.DataFrame, field: str) -> pd.DataFrame:
    if isinstance(raw.columns, pd.MultiIndex):
        if field not in raw.columns.get_level_values(0):
            return pd.DataFrame(index=raw.index)
        selected = raw[field]
    else:
        selected = raw[[field]] if field in raw.columns else pd.DataFrame(index=raw.index)

    if isinstance(selected, pd.Series):
        selected = selected.to_frame()

    selected.index = pd.to_datetime(selected.index).tz_localize(None)
    return selected.sort_index()


def _clean_frame(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame = frame.dropna(how="all")
    frame = frame.loc[:, frame.notna().any(axis=0)]
    frame.columns = [str(column) for column in frame.columns]
    return frame
