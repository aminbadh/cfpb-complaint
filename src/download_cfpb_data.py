"""Download and inspect the CFPB consumer complaints dataset.

This script keeps the first setup lightweight: it can fetch the official CSV ZIP,
extract it into data/raw, and print the discovered columns from the extracted CSV.
"""

from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen


DEFAULT_URL = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url) as response:
        destination.write_bytes(response.read())


def extract_zip(zip_path: Path, destination_dir: Path) -> list[Path]:
    destination_dir.mkdir(parents=True, exist_ok=True)
    extracted_files: list[Path] = []
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            archive.extract(member, path=destination_dir)
            extracted_files.append(destination_dir / member)
    return extracted_files


def find_first_csv(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.suffix.lower() == ".csv":
            return path
    return None


def preview_columns(csv_path: Path, limit: int = 25) -> list[str]:
    with csv_path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.reader(handle)
        return next(reader)[:limit]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download the CFPB complaints dataset")
    parser.add_argument("--url", default=DEFAULT_URL, help="Official CSV ZIP URL")
    parser.add_argument("--download", action="store_true", help="Download the dataset")
    parser.add_argument("--output-dir", default="data/raw", help="Directory for raw data")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    output_dir = Path(args.output_dir)
    zip_path = output_dir / Path(args.url).name

    if args.download or not zip_path.exists():
        print(f"Downloading {args.url} -> {zip_path}")
        download_file(args.url, zip_path)
    else:
        print(f"Using existing archive: {zip_path}")

    extracted_paths = extract_zip(zip_path, output_dir)
    csv_path = find_first_csv(extracted_paths)

    if csv_path is None:
        print("No CSV file was found inside the archive.")
        return 1

    columns = preview_columns(csv_path)
    print(f"Extracted CSV: {csv_path}")
    print("Columns preview:")
    for column in columns:
        print(f"- {column}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())