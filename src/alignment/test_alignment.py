from alignment.general_alignment import NeedlemanWunsch, SmithWaterman, build_weight_matrix
import hashlib
import pytest

def test_aligners():
    matrix = build_weight_matrix("ACGT", 0, 2, 3)

    cases = [
        ("ACG", "ACGT", ("ACG-", "ACGT")),
        ("ACGT", "ACG", ("ACGT", "ACG-")),
        ("ACG", "ACG", ("ACG", "ACG")),
        ("ACGTG", "CCTATG", ("ACG-TG", "CCTATG")),
    ]

    for s, t, expected in cases:
        nw = NeedlemanWunsch(s, t, matrix)
        assert nw.alignment == expected

        h = NeedlemanWunsch(s, t, matrix, hirschberg=True)
        assert h.alignment == expected

def test_needleman():
    matrix = build_weight_matrix("ACGT", 0, 2, 3)

    nw = NeedlemanWunsch("ACCGGTA", "AGGCTG", matrix)

    assert nw.alignment == ("ACCGG-TA", "A--GGCTG")

    assert nw.D[-1, -1] == 9

    assert hashlib.sha256(str(nw).encode()).hexdigest() == "a4ca5d4fa77311f4f48ee10261a0abd993511f1eb0eccdd884450e6318ebac7f"
