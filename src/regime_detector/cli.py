"""Command-line interface for data collection."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from regime_detector.catalog import manifest_universe, symbols


DEFAULT_DAILY_END_DATE = "2026-06-30"
DEFAULT_MONTHLY_END_PERIOD = "202606"


def main() -> None:
    parser = argparse.ArgumentParser(prog="regime-detector")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_parser = subparsers.add_parser("collect", help="Collect raw daily market data.")
    collect_parser.add_argument("--start", default="2000-01-01", help="Start date, YYYY-MM-DD.")
    collect_parser.add_argument(
        "--end",
        default=DEFAULT_DAILY_END_DATE,
        help="End date, YYYY-MM-DD. Defaults to 2026-06-30.",
    )
    collect_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory for raw data files.",
    )

    fred_parser = subparsers.add_parser("collect-fred", help="Collect FRED global regime data.")
    fred_parser.add_argument("--start", default="2000-01-01", help="Start date, YYYY-MM-DD.")
    fred_parser.add_argument(
        "--end",
        default=DEFAULT_DAILY_END_DATE,
        help="End date, YYYY-MM-DD. Defaults to 2026-06-30.",
    )
    fred_parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))

    bok_parser = subparsers.add_parser("collect-bok", help="Collect BOK ECOS Korea macro data.")
    bok_parser.add_argument("--start", default="200001", help="Start period, e.g. 200001.")
    bok_parser.add_argument("--end", default=DEFAULT_MONTHLY_END_PERIOD, help="End period, e.g. 202606.")
    bok_parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))

    kosis_parser = subparsers.add_parser("collect-kosis", help="Collect KOSIS Korea statistics data.")
    kosis_parser.add_argument("--start", default="200001", help="Start period, e.g. 200001.")
    kosis_parser.add_argument("--end", default=DEFAULT_MONTHLY_END_PERIOD, help="End period, e.g. 202606.")
    kosis_parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))

    fundamentals_parser = subparsers.add_parser(
        "collect-fundamentals",
        help="Collect quarterly company fundamentals from Yahoo Finance.",
    )
    fundamentals_parser.add_argument(
        "--end",
        default=DEFAULT_DAILY_END_DATE,
        help="Latest statement date to keep, YYYY-MM-DD. Defaults to 2026-06-30.",
    )
    fundamentals_parser.add_argument("--output-dir", type=Path, default=Path("data/raw/fundamentals"))

    args = parser.parse_args()

    if args.command == "collect":
        run_collection(start=args.start, end=args.end, output_dir=args.output_dir)
    elif args.command == "collect-fred":
        run_fred_collection(start=args.start, end=args.end, output_dir=args.output_dir)
    elif args.command == "collect-bok":
        run_bok_collection(start=args.start, end=args.end, output_dir=args.output_dir)
    elif args.command == "collect-kosis":
        run_kosis_collection(start=args.start, end=args.end, output_dir=args.output_dir)
    elif args.command == "collect-fundamentals":
        run_fundamentals_collection(end=args.end, output_dir=args.output_dir)


def run_collection(start: str, end: str, output_dir: Path) -> None:
    from regime_detector.collectors.yahoo import collect_daily_market_data, write_dataset

    dataset = collect_daily_market_data(symbols=symbols(), start=start, end=end)
    files = write_dataset(dataset=dataset, output_dir=output_dir)

    manifest = {
        "collected_at_utc": datetime.now(UTC).isoformat(),
        "source": "yahoo_finance",
        "start": start,
        "end": end,
        "universe": manifest_universe(),
        "files": files,
    }

    manifest_path = output_dir / "collection_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Wrote {len(files)} data files and manifest to {output_dir}")


def run_fred_collection(start: str, end: str, output_dir: Path) -> None:
    from regime_detector.collectors.fred import FredCollector

    files = FredCollector.from_env().write_series(output_dir=output_dir, start=start, end=end)
    print(f"Wrote {len(files)} FRED file(s) to {output_dir}")


def run_bok_collection(start: str, end: str, output_dir: Path) -> None:
    from regime_detector.collectors.bok import BokEcosCollector

    files = BokEcosCollector.from_env().write_series(output_dir=output_dir, start=start, end=end)
    print(f"Wrote {len(files)} BOK ECOS file(s) to {output_dir}")


def run_kosis_collection(start: str, end: str, output_dir: Path) -> None:
    from regime_detector.collectors.kosis import KosisCollector

    files = KosisCollector.from_env().write_series(output_dir=output_dir, start=start, end=end)
    print(f"Wrote {len(files)} KOSIS file(s) to {output_dir}")


def run_fundamentals_collection(end: str, output_dir: Path) -> None:
    from regime_detector.collectors.fundamentals import YahooFundamentalsCollector

    files = YahooFundamentalsCollector().write_quarterly(output_dir=output_dir, end=end)
    print(f"Wrote {len(files)} fundamentals file(s) to {output_dir}")


if __name__ == "__main__":
    main()
