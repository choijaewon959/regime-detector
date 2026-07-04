"""FRED data collector."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests

from regime_detector.collectors.common import require_env, write_csv
from regime_detector.sources import FredSeries, GLOBAL_RISK_FRED_SERIES


@dataclass(frozen=True)
class FredCollector:
    api_key: str
    base_url: str = "https://api.stlouisfed.org/fred"

    @classmethod
    def from_env(cls, env_name: str = "FRED_API_KEY") -> "FredCollector":
        return cls(api_key=require_env(env_name))

    def collect_series(
        self,
        series: Iterable[FredSeries] = GLOBAL_RISK_FRED_SERIES,
        start: str | None = None,
        end: str | None = "2026-06-30",
    ) -> pd.DataFrame:
        frames: list[pd.DataFrame] = []
        for item in series:
            frame = self._observations(item.series_id, start=start, end=end)
            if not frame.empty:
                frames.append(frame.rename(columns={"value": item.series_id}))

        return pd.concat(frames, axis=1).sort_index() if frames else pd.DataFrame()

    def write_series(
        self,
        output_dir: Path,
        series: Iterable[FredSeries] = GLOBAL_RISK_FRED_SERIES,
        start: str | None = None,
        end: str | None = "2026-06-30",
    ) -> dict[str, str]:
        frame = self.collect_series(series=series, start=start, end=end)
        return {"fred_global_regime": write_csv(frame, output_dir / "fred_global_regime.csv")}

    def _observations(self, series_id: str, start: str | None, end: str | None) -> pd.DataFrame:
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }
        if start:
            params["observation_start"] = start
        if end:
            params["observation_end"] = end

        response = requests.get(f"{self.base_url}/series/observations", params=params, timeout=30)
        response.raise_for_status()
        observations = response.json().get("observations", [])

        frame = pd.DataFrame.from_records(observations)
        if frame.empty:
            return pd.DataFrame()

        frame["date"] = pd.to_datetime(frame["date"])
        frame["value"] = pd.to_numeric(frame["value"].replace(".", pd.NA), errors="coerce")
        return frame.set_index("date")[["value"]].sort_index()
