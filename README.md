# Levenshtein Metrics

A small, dependency-free Python library for measuring how different two strings (or token sequences) are.

Implements the classic **Levenshtein edit distance** together with helpers for normalised similarity and fuzzy lookup. No NumPy, no C extensions, no transitive dependencies — it runs anywhere CPython runs.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)](tests/)

## Features

- **Pure Python** – zero runtime dependencies.
- **Memory efficient** – the dynamic programming matrix is reduced to two rows, so auxiliary space is `O(min(n, m))`.
- **Sequence agnostic** – compares strings, lists of tokens, or any indexable sequence.
- **Unicode safe** – handles non-ASCII input such as `çalıcı` out of the box.
- **Typed and tested** – full type hints and a `pytest` suite covering reference cases.

## Installation

```bash
git clone https://github.com/alcsel/levenshtein-metrics.git
cd Python
python -m pip install -e ".[dev]"
```

## Usage

### Distance

```python
from levenshtein import levenshtein_distance

levenshtein_distance("kitten", "sitting")
# 3

levenshtein_distance(["the", "quick", "fox"], ["the", "slow", "fox"])
# 1
```

### Similarity

```python
from levenshtein import levenshtein_ratio

levenshtein_ratio("kitten", "sitting")
# 0.5714285714285714  (1 - 3 / 7)
```

The ratio is always inside `[0.0, 1.0]`. Identical sequences score `1.0`, and two empty sequences are treated as identical.

### Fuzzy lookup

```python
from levenshtein import closest_match

closest_match("helo", ["hello", "world", "help"])
# ('hello', 0.8)

closest_match("zzzz", ["hello"], threshold=0.9)
# (None, 0.0)
```

### Command line

```bash
python -m levenshtein.cli kitten sitting
# distance:   3
# similarity: 0.5714

python -m levenshtein.cli helo --candidates hello world help
# hello   0.8000
```

After installing the package, the `levenshtein` console script is available with the same arguments. Use `--tokens` to compare whitespace-separated token sequences instead of raw characters.

## API

| Function | Description |
|---|---|
| `levenshtein_distance(source, target) -> int` | Minimum number of insertions, deletions and substitutions. |
| `levenshtein_ratio(source, target) -> float` | Normalised similarity in `[0.0, 1.0]`. |
| `closest_match(query, candidates, *, threshold=0.0) -> tuple` | Best candidate and its score, or `(None, 0.0)`. |

## Complexity

| Metric | Value |
|---|---|
| Time | `O(n * m)` |
| Space | `O(min(n, m))` |

For inputs in the tens of thousands of characters the cost grows quadratically; for those cases prefer an approximate algorithm such as BK-trees over a fixed candidate set.

## Project layout

```
levenshtein/
├── __init__.py     Public exports and package version
├── core.py         Distance, ratio and fuzzy matching
└── cli.py          argparse based command line interface
tests/
└── test_core.py    Unit tests
pyproject.toml      Packaging and tool configuration
```

## Development

```bash
python -m pytest
python -m pytest --cov=levenshtein
```

## License

Released under the [MIT License](LICENSE).
