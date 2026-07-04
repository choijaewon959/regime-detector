from regime_detector.catalog import DEFAULT_UNIVERSE, symbols
from regime_detector.sources import COMPANY_FUNDAMENTAL_SYMBOLS, GLOBAL_RISK_FRED_SERIES


def test_default_universe_contains_kospi_and_memory_leaders() -> None:
    universe_symbols = symbols()

    assert "^KS11" in universe_symbols
    assert "005930.KS" in universe_symbols
    assert "000660.KS" in universe_symbols
    assert len(universe_symbols) == len(DEFAULT_UNIVERSE)


def test_starter_sources_include_global_risk_and_company_fundamentals() -> None:
    fred_series = {series.series_id for series in GLOBAL_RISK_FRED_SERIES}

    assert "VIXCLS" in fred_series
    assert "DEXKOUS" in fred_series
    assert "KORCPIALLMINMEI" in fred_series
    assert "KORPROINDMISMEI" in fred_series
    assert "005930.KS" in COMPANY_FUNDAMENTAL_SYMBOLS
    assert "000660.KS" in COMPANY_FUNDAMENTAL_SYMBOLS
