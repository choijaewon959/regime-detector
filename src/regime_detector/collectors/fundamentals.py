"""Company fundamental data from Yahoo Finance."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import yfinance as yf

from regime_detector.sources import COMPANY_FUNDAMENTAL_SYMBOLS


@dataclass(frozen=True)
class YahooFundamentalsCollector:
    symbols: tuple[str, ...] = COMPANY_FUNDAMENTAL_SYMBOLS

    def collect_quarterly(self, end: str = "2026-06-30") -> dict[str, pd.DataFrame]:
        output: dict[str, pd.DataFrame] = {}
        for symbol in self.symbols:
            ticker = yf.Ticker(symbol)
            output[f"{symbol}_income_quarterly"] = _normalize_statement(ticker.quarterly_financials, end=end)
            output[f"{symbol}_balance_sheet_quarterly"] = _normalize_statement(
                ticker.quarterly_balance_sheet,
                end=end,
            )
            output[f"{symbol}_cashflow_quarterly"] = _normalize_statement(ticker.quarterly_cashflow, end=end)
        return output

    def write_quarterly(self, output_dir: Path, end: str = "2026-06-30") -> dict[str, str]:
        output_dir.mkdir(parents=True, exist_ok=True)
        files: dict[str, str] = {}
        for name, frame in self.collect_quarterly(end=end).items():
            path = output_dir / f"{_safe_name(name)}.csv"
            frame.to_csv(path, index_label="date")
            files[name] = str(path)
        return files


def _normalize_statement(statement: pd.DataFrame, end: str) -> pd.DataFrame:
    if statement.empty:
        return pd.DataFrame()

    frame = statement.transpose()
    frame.index = pd.to_datetime(frame.index).tz_localize(None)
    frame = frame.loc[frame.index <= pd.Timestamp(end)]
    frame.columns = [_safe_name(str(column)) for column in frame.columns]
    return frame.sort_index()


def _safe_name(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace(".", "_")
        .replace("-", "_")
    )
