"""Command line entry point for the levenshtein package."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .core import closest_match, levenshtein_distance, levenshtein_ratio


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="levenshtein",
        description="Measure the edit distance between two strings or tokens.",
    )
    parser.add_argument("source", help="First string or token sequence.")
    parser.add_argument("target", nargs="?", help="Second string or token sequence.")
    parser.add_argument(
        "-c",
        "--candidates",
        nargs="+",
        metavar="WORD",
        help="Compare the first argument against several candidates instead.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.0,
        help="Minimum similarity accepted in candidate mode (default: 0.0).",
    )
    parser.add_argument(
        "--tokens",
        action="store_true",
        help="Split both inputs on whitespace and compare them as token lists.",
    )
    return parser


def _prepare(value: str, as_tokens: bool) -> Sequence:
    return value.split() if as_tokens else value


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    source = _prepare(args.source, args.tokens)

    if args.candidates:
        match, score = closest_match(source, [_prepare(c, args.tokens) for c in args.candidates], threshold=args.threshold)
        if match is None:
            print(f"No candidate reached the similarity threshold of {args.threshold:.2f}.", file=sys.stderr)
            return 1
        rendered = " ".join(match) if args.tokens else match
        print(f"{rendered}\t{score:.4f}")
        return 0

    if args.target is None:
        parser.error("a target string is required unless --candidates is used")

    target = _prepare(args.target, args.tokens)
    distance = levenshtein_distance(source, target)
    ratio = levenshtein_ratio(source, target)

    print(f"distance:   {distance}")
    print(f"similarity: {ratio:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
