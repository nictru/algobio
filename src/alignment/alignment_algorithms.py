from general_alignment import Alignment, build_weight_matrix

class NeedlemanWunsch(Alignment):
    def __init__(self, s: str, t: str, w: dict, is_similarity: bool = False, hirschberg: bool = False):
        super().__init__(s, t, w, Alignment.AlignmentType.GLOBAL, is_similarity, hirschberg)

class SemiGlobal(Alignment):
    def __init__(self, s: str, t: str, w: dict, is_similarity: bool, hirschberg: bool = False):
        super().__init__(s, t, w, Alignment.AlignmentType.SEMI_GLOBAL, is_similarity, hirschberg)

class SmithWaterman(Alignment):
    def __init__(self, s: str, t: str, w: dict, is_similarity: bool, hirschberg: bool = False):
        super().__init__(s, t, w, Alignment.AlignmentType.LOCAL, is_similarity, hirschberg)

def main(description: str, usedClass):
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(type=str, dest="s", help='First sequence')
    parser.add_argument(type=str, dest="t", help='Second sequence')

    parser.add_argument('--match', type=int, default=0, help='Match score')
    parser.add_argument('--indel', type=int, default=2, help='Indel score')
    parser.add_argument('--substitution', type=int, default=3, help='Substitution score')

    parser.add_argument('--similarity', action='store_true', help='Compute similarity instead of distance')
    parser.add_argument('--hirschberg', action='store_true', help='Use Hirschberg algorithm')

    args = parser.parse_args()

    s = args.s
    t = args.t

    alphabet = set(s + t)

    w = build_weight_matrix(alphabet, args.match, args.indel, args.substitution)

    nw = usedClass(s, t, w, args.similarity, args.hirschberg)
    print(nw)