from needleman_wunsch import NeedlemanWunsch, build_weight_matrix
from hirschberg import Hirschberg

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
