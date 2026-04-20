"""Fetch a working subset of CFPB complaints via the official API.

This script pulls recent complaints with narratives using the official API,
which is much faster and lighter than downloading the full 1.8GB archive.

The API is documented at: https://cfpb.github.io/api/ccdb/api.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

DEFAULT_BASE_URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
DEFAULT_OUTPUT_FILE = "data/raw/complaints_api_sample.json"


def build_api_url(
    base_url: str,
    limit: int = 100,
    offset: int = 0,
    has_narrative: bool = True,
    sort_by: str = "created_date_desc",
) -> str:
    """Build an API query URL with sensible defaults for EDA."""
    params = {
        "size": limit,
        "from": offset,
        "format": "json",
        "sort": sort_by,
    }
    if has_narrative:
        params["has_narrative"] = "yes"
    
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"


def fetch_page(url: str, timeout: int = 30) -> dict:
    """Fetch one page of API results."""
    with urlopen(url, timeout=timeout) as response:
        return json.loads(response.read())


def fetch_all(
    base_url: str,
    total_records: int = 10000,
    page_size: int = 100,
    has_narrative: bool = True,
) -> list[dict]:
    """Fetch multiple pages from the API."""
    all_complaints = []
    pages_to_fetch = (total_records + page_size - 1) // page_size
    
    for page_num in range(pages_to_fetch):
        offset = page_num * page_size
        url = build_api_url(base_url, limit=page_size, offset=offset, has_narrative=has_narrative)
        
        print(f"Fetching page {page_num + 1}/{pages_to_fetch} (offset {offset})...")
        try:
            response = fetch_page(url)
            complaints = response.get("hits", {}).get("hits", [])
            
            if not complaints:
                print("No more records returned. Stopping.")
                break
            
            all_complaints.extend(complaints)
            total_hit = response.get("hits", {}).get("total", 0)
            print(f"  Got {len(complaints)} records. Total available: {total_hit}")
        except Exception as e:
            print(f"Error fetching page {page_num + 1}: {e}")
            break
    
    return all_complaints


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch CFPB complaints via the official API (lightweight alternative to full download)."
    )
    parser.add_argument(
        "--records",
        type=int,
        default=10000,
        help="Total number of records to fetch (default 10000, a good working subset).",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="API page size (default 100).",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output JSON file (default {DEFAULT_OUTPUT_FILE}).",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API base URL (default {DEFAULT_BASE_URL}).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    
    print(f"Fetching up to {args.records} CFPB complaints with narratives...")
    complaints = fetch_all(
        base_url=args.base_url,
        total_records=args.records,
        page_size=args.page_size,
        has_narrative=True,
    )
    
    if not complaints:
        print("No records fetched. Check your connection and API URL.")
        return 1
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("w") as f:
        json.dump(complaints, f, indent=2)
    
    print(f"\nFetched {len(complaints)} records.")
    print(f"Saved to {output_path}")
    
    # Print a quick sample
    if complaints:
        first = complaints[0].get("_source", {})
        print("\nFirst record fields:")
        for key in sorted(first.keys())[:10]:
            val = first[key]
            if isinstance(val, str):
                val = val[:50] + "..." if len(val) > 50 else val
            print(f"  {key}: {val}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
