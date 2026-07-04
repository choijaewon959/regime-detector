from regime_detector.catalog import DEFAULT_UNIVERSE, symbols


def test_default_universe_contains_kospi_and_memory_leaders() -> None:
    universe_symbols = symbols()

    assert "^KS11" in universe_symbols
    assert "005930.KS" in universe_symbols
    assert "000660.KS" in universe_symbols
    assert len(universe_symbols) == len(DEFAULT_UNIVERSE)
