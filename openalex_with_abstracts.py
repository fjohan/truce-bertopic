#!/usr/bin/env python3
"""
Fetch OpenAlex works for a search query and output a TSV with title and reconstructed abstract.

Defaults:
- Filters to journal articles (type:journal-article) unless --filters is provided.
- Outputs tab-separated values with columns: title, abstract.

Usage examples:
  # Phrase search (recommended), default journal articles, TSV output
  python openalex_works_with_abstracts_tsv.py --query "knowledge system" --out works.tsv

  # Token search (no quotes)
  python openalex_works_with_abstracts_tsv.py --query "knowledge system" --no-quotes --out works.tsv

  # Custom filters (overrides default)
  python openalex_works_with_abstracts_tsv.py --query "knowledge system" \
      --filters "type:journal-article,from_publication_date:2018-01-01,language:en" \
      --limit 300 --per-page 200 --out works.tsv

  # Skip works without abstracts
  python openalex_works_with_abstracts_tsv.py --query "knowledge system" --skip-missing --out works.tsv
"""

import argparse
import csv
import sys
import time
from typing import Dict, Iterable, List, Optional

import requests

API_URL = "https://api.openalex.org/works"


def reconstruct_abstract(inv_index: Optional[Dict[str, List[int]]]) -> Optional[str]:
    """Rebuild abstract text from OpenAlex abstract_inverted_index."""
    if not inv_index:
        return None
    try:
        max_pos = max(p for positions in inv_index.values() for p in positions)
    except ValueError:
        return None
    words = [""] * (max_pos + 1)
    for token, positions in inv_index.items():
        for p in positions:
            words[p] = token
    text = " ".join(w for w in words if w).strip()
    return text or None


def fetch_works(
    query: str,
    per_page: int = 200,
    limit: int = 1000,
    phrase: bool = True,
    sleep: float = 0.1,
    select: str = "display_name,abstract_inverted_index",
    filters: Optional[str] = None,
) -> Iterable[Dict]:
    """
    Generator yielding OpenAlex work objects for the query.

    - Uses cursor-based pagination.
    - Wraps query in quotes for phrase search unless phrase=False.
    - Applies 'select' to minimize payload size.
    - If 'filters' is None, defaults to 'type:journal-article'.
    """
    params = {
        "per-page": str(per_page),
        "cursor": "*",
        "select": select,
        "search": f'"{query}"' if phrase else query,
        "filter": filters if filters is not None else "type:article",
    }

    fetched = 0
    while True:
        r = requests.get(API_URL, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        for item in data.get("results", []):
            yield item
            fetched += 1
            if fetched >= limit:
                return
        next_cursor = data.get("meta", {}).get("next_cursor")
        if not next_cursor:
            return
        params["cursor"] = next_cursor
        if sleep:
            time.sleep(sleep)  # be nice to the API


def write_tsv(rows: List[Dict], out_path: str) -> None:
    # Only two columns, tab-separated
    fieldnames = ["title", "abstract"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    ap = argparse.ArgumentParser(description="Fetch OpenAlex works and write TSV (title, abstract).")
    ap.add_argument("--query", required=True, help='Search query, e.g. "knowledge system"')
    ap.add_argument("--out", required=True, help="Output TSV path")
    ap.add_argument("--limit", type=int, default=1000, help="Max number of works to fetch (default: 1000)")
    ap.add_argument("--per-page", type=int, default=200, help="Results per page (default: 200)")
    ap.add_argument("--no-quotes", action="store_true", help="Use token search (no quoted phrase)")
    ap.add_argument("--sleep", type=float, default=0.1, help="Seconds to sleep between pages (default: 0.1)")
    ap.add_argument("--filters", default=None,
                    help="OpenAlex filter string; if omitted, defaults to 'type:article'. "
                         "Example: 'type:article,from_publication_date:2018-01-01,language:en'")
    ap.add_argument("--skip-missing", action="store_true",
                    help="Skip works without an abstract (otherwise abstract column is empty)")
    args = ap.parse_args()

    try:
        works_iter = fetch_works(
            query=args.query,
            per_page=args.per_page,
            limit=args.limit,
            phrase=not args.no_quotes,
            sleep=args.sleep,
            filters=args.filters,  # None -> defaults to journal articles inside fetch_works
        )

        rows: List[Dict] = []
        for w in works_iter:
            title = (w.get("display_name") or "").strip()
            abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
            if args.skip_missing and not abstract:
                continue
            rows.append({"title": title, "abstract": abstract or ""})

        write_tsv(rows, args.out)
        print(f"Wrote {len(rows)} rows to {args.out}")
        if rows and any(r["abstract"] for r in rows):
            print("Note: Abstract text is copyrighted by publishers. Do not redistribute this TSV.")

    except requests.HTTPError as e:
        print(f"HTTP error: {e} — URL: {e.request.url}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()



