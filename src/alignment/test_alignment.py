from needleman_wunsch import NeedlemanWunsch, build_weight_matrix, main
from hirschberg import Hirschberg
import hashlib
import pytest

def test_aligners():
    matrix = build_weight_matrix("ACGT", 0, 2, 3)

    cases = [
       # ("ACG", "ACGT", ("ACG-", "ACGT")),
        ("ACGT", "ACG", ("ACGT", "ACG-")),
        ("ACG", "ACG", ("ACG", "ACG")),
        ("ACGTG", "CCTATG", ("ACG-TG", "CCTATG")),
    ]

    for s, t, expected in cases:
        nw = NeedlemanWunsch(s, t, matrix)
        assert nw.alignment == expected

        h = Hirschberg(s, t, matrix)
        assert h.alignment == expected

def test_needleman():
    matrix = build_weight_matrix("ACGT", 0, 2, 3)

    nw = NeedlemanWunsch("ACCGGTA", "AGGCTG", matrix)

    assert nw.alignment == ("ACCGG-TA", "A--GGCTG")

    assert nw.D[-1, -1] == 9

    assert hashlib.sha256(str(nw).encode()).hexdigest() == "a4ca5d4fa77311f4f48ee10261a0abd993511f1eb0eccdd884450e6318ebac7f"

def test_main():
    for algorithm in [NeedlemanWunsch, Hirschberg]:
        with pytest.raises(SystemExit):
            main("Algorithm", algorithm)
