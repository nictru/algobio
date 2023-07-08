from alignment_algorithms import NeedlemanWunsch, SmithWaterman, build_weight_matrix
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

    assert hashlib.sha256(str(nw).encode()).hexdigest() == "0c03e38e4d5d99d653b64ad7de4a9fd1e4cc5abbe4ffb01e16f52957ae473908"
