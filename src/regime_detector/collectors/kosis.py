"""KOSIS Open API collector."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests

from regime_detector.collectors.common import require_env, write_csv
from regime_detector.sources import KOREA_MACRO_KOSIS_SERIES, KosisSeries


@dataclass(frozen=True)
class KosisCollector:
    api_key: str
    base_url: str = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

    @classmethod
    def from_env(cls, env_name: str = "KOSIS_API_KEY") -> "KosisCollector":
        return cls(api_key=require_env(env_name))

    def collect_series(
        self,
        series: Iterable[KosisSeries] = KOREA_MACRO_KOSIS_SERIES,
        start: str = "200001",
        end: str = "202606",
    ) -> pd.DataFrame:
        frames: list[pd.DataFrame] = []
        for item in series:
            frame = self._statistics_data(item, start=start, end=end)
            if not frame.empty:
                frames.append(frame.rename(columns={"value": item.item_id}))

        return pd.concat(frames, axis=1).sort_index() if frames else pd.DataFrame()

    def write_series(
        self,
        output_dir: Path,
        series: Iterable[KosisSeries] = KOREA_MACRO_KOSIS_SERIES,
        start: str = "200001",
        end: str = "202606",
    ) -> dict[str, str]:
        frame = self.collect_series(series=series, start=start, end=end)
        return {"kosis_korea_macro": write_csv(frame, output_dir / "kosis_korea_macro.csv")}

    def _statistics_data(self, item: KosisSeries, start: str, end: str) -> pd.DataFrame:
        params = {
            "method": "getList",
            "apiKey": self.api_key,
            "format": "json",
            "jsonVD": "Y",
            "userStatsId": f"{item.org_id}/{item.table_id}",
            "prdSe": item.period,
            "startPrdDe": start,
            "endPrdDe": end,
            "orgId": item.org_id,
            "tblId": item.table_id,
            "itmId": item.item_id,
            "objL1": item.obj_l1,
        }
        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        rows = response.json()

        frame = pd.DataFrame.from_records(rows)
        if frame.empty:
            return pd.DataFrame()

        value_column = "DT" if "DT" in frame.columns else "DATA_VALUE"
        frame["date"] = pd.to_datetime(frame["PRD_DE"], errors="coerce")
        frame["value"] = pd.to_numeric(frame[value_column], errors="coerce")
        return frame.set_index("date")[["value"]].sort_index()
