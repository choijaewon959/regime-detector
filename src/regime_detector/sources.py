"""Starter data source definitions for regime research."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FredSeries:
    series_id: str
    name: str
    role: str


@dataclass(frozen=True)
class BokSeries:
    stat_code: str
    item_code: str
    cycle: str
    name: str
    role: str


@dataclass(frozen=True)
class KosisSeries:
    org_id: str
    table_id: str
    item_id: str
    period: str
    name: str
    role: str
    obj_l1: str = "ALL"


GLOBAL_RISK_FRED_SERIES: tuple[FredSeries, ...] = (
    FredSeries("VIXCLS", "CBOE VIX", "global_risk"),
    FredSeries("DGS2", "US 2Y Treasury Yield", "global_rates"),
    FredSeries("DGS10", "US 10Y Treasury Yield", "global_rates"),
    FredSeries("T10Y2Y", "US 10Y minus 2Y Treasury Spread", "global_rates"),
    FredSeries("FEDFUNDS", "Effective Federal Funds Rate", "global_liquidity"),
    FredSeries("DTWEXBGS", "Trade Weighted US Dollar Index", "global_fx"),
    FredSeries("BAMLH0A0HYM2", "US High Yield Option-Adjusted Spread", "global_credit"),
    FredSeries("DEXKOUS", "KRW/USD Exchange Rate", "korea_fx"),
    FredSeries("KORCPIALLMINMEI", "Korea CPI", "korea_inflation"),
    FredSeries("KORPROINDMISMEI", "Korea Industrial Production", "korea_growth"),
    FredSeries("IR3TIB01KRM156N", "Korea 3M Interbank Rate", "korea_rates"),
)


COMPANY_FUNDAMENTAL_SYMBOLS: tuple[str, ...] = (
    "005930.KS",
    "000660.KS",
    "MU",
    "NVDA",
    "TSM",
)


# Fill these with confirmed ECOS/KOSIS table IDs after choosing exact official series.
KOREA_MACRO_BOK_SERIES: tuple[BokSeries, ...] = ()
KOREA_MACRO_KOSIS_SERIES: tuple[KosisSeries, ...] = ()
