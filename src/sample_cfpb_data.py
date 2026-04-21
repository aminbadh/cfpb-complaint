"""Sample CFPB complaints CSV without loading the entire file into memory.

This script reads the large CSV in chunks and pulls a random sample,
then saves it to a smaller working file. This avoids the system crash from
loading the full 1.8GB dataset.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def find_csv(search_dir: Path) -> Path | None:
    """Find the first CSV file in a directory."""
    csv_files = sorted(search_dir.glob("*.csv"))
    return csv_files[0] if csv_files else None


def sample_csv_chunked(
    csv_path: Path,
    output_path: Path,
    sample_size: int = 50000,
    chunksize: int = 10000,
) -> int:
    """Read CSV in chunks and save a random sample to output_path."""
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 1

    print(f"Reading {csv_path} in chunks of {chunksize}...")
    
    chunks = []
    row_count = 0
    # Keep memory bounded while still reading enough rows for a good sample.
    max_rows_to_read = max(sample_size * 2, 200000)
    
    # Read in chunks to avoid memory overload
    for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False):
        chunks.append(chunk)
        row_count += len(chunk)
        print(f"  Read {row_count} rows so far...")
        
        # Stop early once we reach the configurable safety limit.
        if row_count >= max_rows_to_read:
            print(f"  Stopping at {row_count} rows (memory safety).")
            break
    
    if not chunks:
        print("No data read from CSV.")
        return 1
    
    # Concatenate and sample
    print(f"Combining {len(chunks)} chunks...")
    df = pd.concat(chunks, ignore_index=True)
    
    print(f"Total rows read: {len(df)}")
    print(f"Sampling {sample_size} rows...")
    sample_df = df.sample(n=min(sample_size, len(df)), random_state=42)
    
    # Save the sample
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample_df.to_csv(output_path, index=False)
    
    print(f"Saved {len(sample_df)} rows to {output_path}")
    print(f"Output file size: {output_path.stat().st_size / (1024**2):.2f} MB")
    
    # Print column info
    print(f"\nColumns ({len(sample_df.columns)}):")
    for col in list(sample_df.columns)[:15]:
        print(f"  - {col}")
    if len(sample_df.columns) > 15:
        print(f"  ... and {len(sample_df.columns) - 15} more")
    
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sample a large CFPB CSV without loading it all into memory."
    )
    parser.add_argument(
        "--input-dir",
        default="data/raw",
        help="Directory containing the complaints CSV.",
    )
    parser.add_argument(
        "--output",
        default="data/processed/complaints_sample.csv",
        help="Output CSV file path.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=50000,
        help="Number of rows to sample (default 50000).",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=10000,
        help="CSV read chunk size (default 10000).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    
    input_dir = Path(args.input_dir)
    csv_path = find_csv(input_dir)
    
    if csv_path is None:
        print(f"No CSV file found in {input_dir}")
        return 1
    
    output_path = Path(args.output)
    
    return sample_csv_chunked(
        csv_path=csv_path,
        output_path=output_path,
        sample_size=args.sample_size,
        chunksize=args.chunksize,
    )


if __name__ == "__main__":
    raise SystemExit(main())
