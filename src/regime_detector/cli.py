"""Command-line interface for data collection."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from regime_detector.catalog import manifest_universe, symbols


def main() -> None:
    parser = argparse.ArgumentParser(prog="regime-detector")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_parser = subparsers.add_parser("collect", help="Collect raw daily market data.")
    collect_parser.add_argument("--start", default="2000-01-01", help="Start date, YYYY-MM-DD.")
    collect_parser.add_argument("--end", default=None, help="Optional end date, YYYY-MM-DD.")
    collect_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory for raw data files.",
    )

    args = parser.parse_args()

    if args.command == "collect":
        run_collection(start=args.start, end=args.end, output_dir=args.output_dir)


def run_collection(start: str, end: str | None, output_dir: Path) -> None:
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


if __name__ == "__main__":
    main()
