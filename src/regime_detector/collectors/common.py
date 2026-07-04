"""Shared collector helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pandas as pd


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def write_csv(frame: pd.DataFrame, path: Path, index_label: str = "date") -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index_label=index_label)
    return str(path)


def records_to_frame(records: list[dict[str, Any]], date_column: str, value_column: str) -> pd.DataFrame:
    frame = pd.DataFrame.from_records(records)
    if frame.empty:
        return pd.DataFrame()

    frame[date_column] = pd.to_datetime(frame[date_column])
    frame[value_column] = pd.to_numeric(frame[value_column], errors="coerce")
    return frame.set_index(date_column)[[value_column]].sort_index()
