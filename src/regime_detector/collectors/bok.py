"""Bank of Korea ECOS collector."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests

from regime_detector.collectors.common import require_env, write_csv
from regime_detector.sources import BokSeries, KOREA_MACRO_BOK_SERIES


@dataclass(frozen=True)
class BokEcosCollector:
    api_key: str
    language: str = "en"
    base_url: str = "https://ecos.bok.or.kr/api"

    @classmethod
    def from_env(cls, env_name: str = "BOK_ECOS_API_KEY") -> "BokEcosCollector":
        return cls(api_key=require_env(env_name))

    def collect_series(
        self,
        series: Iterable[BokSeries] = KOREA_MACRO_BOK_SERIES,
        start: str = "200001",
        end: str = "202606",
    ) -> pd.DataFrame:
        frames: list[pd.DataFrame] = []
        for item in series:
            frame = self._statistic_search(item, start=start, end=end)
            if not frame.empty:
                frames.append(frame.rename(columns={"value": item.item_code or item.stat_code}))

        return pd.concat(frames, axis=1).sort_index() if frames else pd.DataFrame()

    def write_series(
        self,
        output_dir: Path,
        series: Iterable[BokSeries] = KOREA_MACRO_BOK_SERIES,
        start: str = "200001",
        end: str = "202606",
    ) -> dict[str, str]:
        frame = self.collect_series(series=series, start=start, end=end)
        return {"bok_korea_macro": write_csv(frame, output_dir / "bok_korea_macro.csv")}

    def _statistic_search(self, item: BokSeries, start: str, end: str) -> pd.DataFrame:
        item_code = item.item_code or "?"
        url = (
            f"{self.base_url}/StatisticSearch/{self.api_key}/json/{self.language}/"
            f"1/100000/{item.stat_code}/{item.cycle}/{start}/{end}/{item_code}"
        )
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        rows = response.json().get("StatisticSearch", {}).get("row", [])

        frame = pd.DataFrame.from_records(rows)
        if frame.empty:
            return pd.DataFrame()

        frame["date"] = pd.to_datetime(frame["TIME"], errors="coerce")
        frame["value"] = pd.to_numeric(frame["DATA_VALUE"], errors="coerce")
        return frame.set_index("date")[["value"]].sort_index()
