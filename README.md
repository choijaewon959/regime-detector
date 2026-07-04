# regime-detector

Data collection scaffold for studying whether the Korean equity market is entering a new AI memory supercycle regime or behaving like prior market regimes.

The project is intentionally small for now. It only collects raw daily market data that can later support regime detection and trading strategy research.

## What It Collects

The default universe focuses on:

- Korean market benchmark: KOSPI
- Korean memory leaders: Samsung Electronics and SK hynix
- Korean macro/FX context: USD/KRW
- Global AI and semiconductor proxies: NASDAQ 100, Philadelphia Semiconductor Index, SOXX, NVIDIA, Micron, TSMC

Data is downloaded from Yahoo Finance through `yfinance`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Collect Data

```bash
python -m regime_detector collect --start 2000-01-01
```

By default, files are written to:

```text
data/raw/
```

The collector writes:

- `prices_daily.csv`: adjusted daily close prices
- `volumes_daily.csv`: daily volume where available
- `returns_daily.csv`: daily percentage returns
- `collection_manifest.json`: run metadata and ticker mapping

## Scheduled Job

The GitHub Actions workflow in `.github/workflows/collect-data.yml` can run the collector manually or on a weekly schedule. It uploads the collected files as a workflow artifact.

## Repository

This project is intended for:

[choijaewon959/regime-detector](https://github.com/choijaewon959/regime-detector.git)
