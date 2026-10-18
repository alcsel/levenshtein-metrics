"""Core edit-distance primitives."""

from __future__ import annotations

from typing import Sequence

__all__ = [
    "levenshtein_distance",
    "levenshtein_ratio",
    "closest_match",
]

_OPERATION_COST = 1


def levenshtein_distance(source: Sequence, target: Sequence) -> int:
    """Return the Levenshtein edit distance between two sequences.

    Works with any indexable sequence of hashable-free comparable items,
    which means both strings and lists of tokens are accepted.

    The implementation keeps only two rows of the dynamic programming
    matrix in memory, so the auxiliary space is O(min(n, m)).
    """
    if source is target:
        return 0

    if len(source) < len(target):
        source, target = target, source

    if not target:
        return len(source)

    previous = list(range(len(target) + 1))
    current = [0] * (len(target) + 1)

    for i, source_item in enumerate(source, start=1):
        current[0] = i
        for j, target_item in enumerate(target, start=1):
            substitution = previous[j - 1]
            if source_item != target_item:
                substitution += _OPERATION_COST
            current[j] = min(
                previous[j] + _OPERATION_COST,
                current[j - 1] + _OPERATION_COST,
                substitution,
            )
        previous, current = current, previous

    return previous[len(target)]


def levenshtein_ratio(source: Sequence, target: Sequence) -> float:
    """Return a normalised similarity score in the inclusive range [0.0, 1.0].

    A score of ``1.0`` means the sequences are identical and ``0.0`` means
    they share nothing, mirroring the convention used by fuzzy-matching
    libraries. Two empty sequences are considered identical.
    """
    longest = max(len(source), len(target))
    if longest == 0:
        return 1.0

    distance = levenshtein_distance(source, target)
    return 1.0 - (distance / longest)


def closest_match(
    query: Sequence,
    candidates: Sequence[Sequence],
    *,
    threshold: float = 0.0,
) -> tuple[Sequence | None, float]:
    """Return the candidate with the highest similarity to ``query``.

    ``threshold`` is the minimum similarity required for a candidate to be
    accepted. When no candidate reaches it, ``(None, 0.0)`` is returned.
    Ties are resolved in favour of the earliest candidate.
    """
    best_match: Sequence | None = None
    best_score = 0.0

    for candidate in candidates:
        score = levenshtein_ratio(query, candidate)
        if score > best_score:
            best_match = candidate
            best_score = score

    if best_score < threshold:
        return None, 0.0

    return best_match, best_score
