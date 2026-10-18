"""Dependency-free Levenshtein edit distance and similarity metrics."""

from __future__ import annotations

from .core import closest_match, levenshtein_distance, levenshtein_ratio

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "closest_match",
    "levenshtein_distance",
    "levenshtein_ratio",
]
