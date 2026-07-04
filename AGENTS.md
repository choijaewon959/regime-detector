# AGENTS.md

This project studies Korean equity market regimes, especially whether the current KOSPI environment is a new AI-driven memory supercycle or resembles earlier regimes.

Keep the project simple and research-oriented. The current stage is data collection only. Do not add modeling, trading signals, backtests, dashboards, or optimization logic unless explicitly requested.

Core research focus:

- KOSPI and KOSPI 200 as Korean market benchmarks.
- Samsung Electronics and SK hynix as dominant Korean memory/AI-cycle exposures.
- USD/KRW, rates, liquidity, exports, and macro data as regime context.
- Global AI and semiconductor proxies such as NASDAQ 100, SOX, SOXX, NVIDIA, Micron, and TSMC.
- Later datasets may include Korean macro series from BOK ECOS/KOSIS, semiconductor sales, memory prices, equipment billings, company fundamentals, and AI demand proxies.

Engineering guidelines:

- Prefer small, readable Python modules.
- Keep raw source data separate from derived features.
- CSV is acceptable for the current daily dataset; consider Parquet only when scale or pipeline needs justify it.
- Make collectors reproducible and easy to run locally and in GitHub Actions.
- Preserve clear metadata/manifests for every collection run.
- Avoid premature abstraction.

Useful commands:

```bash
python -m pytest
PYTHONPATH=src python -m regime_detector --help
PYTHONPATH=src python -m regime_detector collect --start 2000-01-01 --end 2026-06-30
```
