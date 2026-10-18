from __future__ import annotations

import pytest

from levenshtein import closest_match, levenshtein_distance, levenshtein_ratio


class TestLevenshteinDistance:
    def test_identical_strings_have_zero_distance(self):
        assert levenshtein_distance("kitten", "kitten") == 0

    def test_empty_source_returns_target_length(self):
        assert levenshtein_distance("", "abcd") == 4

    def test_empty_target_returns_source_length(self):
        assert levenshtein_distance("abcd", "") == 4

    def test_both_empty_returns_zero(self):
        assert levenshtein_distance("", "") == 0

    @pytest.mark.parametrize(
        ("source", "target", "expected"),
        [
            ("kitten", "sitting", 3),
            ("flaw", "lawn", 2),
            ("saturday", "sunday", 3),
            ("gumbo", "gambol", 2),
            ("a", "b", 1),
            ("abc", "abc", 0),
        ],
    )
    def test_reference_pairs(self, source, target, expected):
        assert levenshtein_distance(source, target) == expected

    def test_is_symmetric(self):
        assert levenshtein_distance("kitten", "sitting") == levenshtein_distance("sitting", "kitten")

    def test_accepts_token_lists(self):
        assert levenshtein_distance(["a", "b", "c"], ["a", "x", "c"]) == 1

    def test_handles_unicode(self):
        assert levenshtein_distance("çalıcı", "calici") == 3

    def test_long_inputs_do_not_exhaust_memory(self):
        left = "a" * 2000
        right = "b" * 2000
        assert levenshtein_distance(left, right) == 2000


class TestLevenshteinRatio:
    def test_identical_strings_score_one(self):
        assert levenshtein_ratio("abc", "abc") == 1.0

    def test_two_empty_strings_are_identical(self):
        assert levenshtein_ratio("", "") == 1.0

    def test_score_is_bounded(self):
        score = levenshtein_ratio("abc", "xyz")
        assert 0.0 <= score <= 1.0

    def test_known_ratio(self):
        assert levenshtein_ratio("kitten", "sitting") == pytest.approx(1 - 3 / 7)

    def test_empty_against_non_empty_scores_zero(self):
        assert levenshtein_ratio("", "abcd") == 0.0


class TestClosestMatch:
    def test_picks_the_nearest_candidate(self):
        match, score = closest_match("helo", ["hello", "world", "help"])
        assert match == "hello"
        assert score == pytest.approx(0.8)

    def test_threshold_rejects_weak_matches(self):
        match, score = closest_match("zzzz", ["hello"], threshold=0.9)
        assert match is None
        assert score == 0.0

    def test_returns_none_for_empty_candidates(self):
        assert closest_match("abc", []) == (None, 0.0)

    def test_threshold_is_inclusive(self):
        match, _ = closest_match("abc", ["abd"], threshold=2 / 3)
        assert match == "abd"
