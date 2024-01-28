from knuth_morris_pratt import (
    __compute_shift_table_z__,
    __compute_shift_table_z_mathematical__,
    __compute_shift_table__,
    kmp,
)
from boyer_moore import boyer_moore_bc, boyer_moore_galil, boyer_moore_gs
from naive import naive, naive2, main
from borders import actual_border, real_borders, borders
from z_boxes import z_boxes
import pytest


def test_shift_table_relations():
    words = ["abc", "bbababbaba"]
    for word in words:
        assert __compute_shift_table_z__(
            word
        ) == __compute_shift_table_z_mathematical__(word)
        assert all(
            with_z <= without_z
            for with_z, without_z in zip(
                __compute_shift_table_z__(word), __compute_shift_table__(word)
            )
        )


def test_shift_table():
    cases = [
        ("abc", [-1, 0, 0, 0]),
        ("abababab", [-1, 0, 0, 1, 2, 3, 4, 5, 6]),
        ("abababac", [-1, 0, 0, 1, 2, 3, 4, 5, 0]),
    ]

    for word, expected in cases:
        assert __compute_shift_table__(word) == expected


def test_search_algorithms():
    cases = [
        ("abc", "abc", True),
        ("abc", "ab", True),
        ("abc", "bc", True),
        ("abc", "ac", False),
    ]

    algorithms = [naive, naive2, kmp, boyer_moore_bc, boyer_moore_galil, boyer_moore_gs]

    for text, pattern, expected in cases:
        for algorithm in algorithms:
            assert algorithm(text, pattern) == expected


def test_borders():
    cases = [("abc", "", [""], ["", "abc"])]

    for text, actual_expected, real_expected, all_expected in cases:
        assert borders(text) == all_expected
        assert real_borders(text) == real_expected
        assert actual_border(text) == actual_expected


def test_z_boxes():
    cases = [
        ("abc", [0, 0, 0]),
        ("abaabaabab", [0, 0, 1, 6, 0, 1, 3, 0, 2, 0]),
    ]

    for text, expected in cases:
        assert z_boxes(text) == expected


def test_naive_main():
    with pytest.raises(SystemExit):
        main()
