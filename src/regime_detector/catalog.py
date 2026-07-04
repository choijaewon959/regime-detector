"""Default data universe for the regime-detector project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    symbol: str
    name: str
    role: str
    market: str


DEFAULT_UNIVERSE: tuple[Instrument, ...] = (
    Instrument("^KS11", "KOSPI Composite Index", "korea_equity_benchmark", "KR"),
    Instrument("005930.KS", "Samsung Electronics", "korea_memory_leader", "KR"),
    Instrument("000660.KS", "SK hynix", "korea_memory_leader", "KR"),
    Instrument("USDKRW=X", "USD/KRW", "fx_context", "FX"),
    Instrument("^NDX", "NASDAQ 100", "global_growth_proxy", "US"),
    Instrument("^SOX", "Philadelphia Semiconductor Index", "semiconductor_cycle_proxy", "US"),
    Instrument("SOXX", "iShares Semiconductor ETF", "semiconductor_cycle_proxy", "US"),
    Instrument("NVDA", "NVIDIA", "ai_leader_proxy", "US"),
    Instrument("MU", "Micron Technology", "memory_cycle_proxy", "US"),
    Instrument("TSM", "Taiwan Semiconductor Manufacturing", "foundry_cycle_proxy", "US"),
)


def symbols() -> list[str]:
    return [instrument.symbol for instrument in DEFAULT_UNIVERSE]


def manifest_universe() -> list[dict[str, str]]:
    return [
        {
            "symbol": instrument.symbol,
            "name": instrument.name,
            "role": instrument.role,
            "market": instrument.market,
        }
        for instrument in DEFAULT_UNIVERSE
    ]
