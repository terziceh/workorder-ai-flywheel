#!/usr/bin/env python3
"""CLI for generating public synthetic work-order data."""

from __future__ import annotations

import argparse

from workorder_ai.synthetic import generate_workorders, write_workorders_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="sample_data/synthetic_workorders.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = generate_workorders(rows=args.rows, seed=args.seed)
    output = write_workorders_csv(records, args.output)
    print(f"Generated {len(records):,} synthetic work orders at {output}")


if __name__ == "__main__":
    main()
