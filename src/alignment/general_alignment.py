import numpy as np
from typing import Dict, Set
from enum import Enum

def build_weight_matrix(alphabet: str | Set[str], match: int, indel: int, substitution: int):
    """
    Builds a weight matrix for the given alphabet and weights.
    """
    w = {
        a: {b: match if a == b else substitution for b in alphabet} for a in alphabet
    }

    w['-'] = {a: indel for a in alphabet}

    for a in alphabet:
        w[a]['-'] = indel

    return w

class Alignment:
    class Direction(Enum):
        LEFT = 5
        DIAG = 6
        UP = 7
        NONE = 8

    class AlignmentType(Enum):
        GLOBAL = 0
        SEMI_GLOBAL = 1
        LOCAL = 2

    def __init__(self, s: str, t: str, w: Dict[str, Dict[str, int]], type: AlignmentType, is_similarity: bool, hirschberg: bool = False) -> None:
        self.s = s
        self.t = t
        self.w = w
        self.type = type
        self.is_similarity = is_similarity
        self.hirschberg = hirschberg

        if hirschberg and not type == Alignment.AlignmentType.GLOBAL:
            raise ValueError("Hirschberg algorithm has only been implemented for global alignment")

        if type == Alignment.AlignmentType.SEMI_GLOBAL:
            raise UserWarning("Semi-global alignment has not been tested yet")

        weights = [w[a][b] for a in w for b in w[a]]
        min_weight = min(weights)

        if not is_similarity and min_weight < 0:
            raise ValueError("Weight matrix must be non-negative for distance computation")

        self.alignment = self.__align__(s, t) if not hirschberg else self.__align_hirschberg__(s, t)

    def __align__(self, s: str, t: str):
        """
        Performs the alignment by computing the full score and backtracking matrices.
        """
        D, B = self.__generate_matrix__(s, t)

        self.D = D
        self.B = B

        return self.__backtracking__(D, B, s, t)

    def __align_hirschberg__(self, s: str, t: str):
        """
        Computes the alignment recursively using the Hirschberg algorithm.
        Has only been tested for global alignment.
        """
        delim = len(s)//2

        s1 = s[:delim]
        t1 = t
        D1, B1 = self.__generate_matrix__(s1, t1)

        s2 = s[delim:][::-1]
        t2 = t[::-1]
        D2, B2 = self.__generate_matrix__(s2, t2)

        summarized = D1[-1] + D2[-1][::-1]
        min_index = summarized.argmax() if self.is_similarity else summarized.argmin()
        
        if len(s1) == 1:
            end_index = min_index+1
            alignment1 = self.__backtracking__(D1[:,:end_index], B1[:,:end_index], s1, t1[:end_index])
        else:
            alignment1 = self.__align_hirschberg__(s[:delim], t[:min_index])

        if len(s2) == 1:
            end_index = len(t2)-min_index+1
            alignment2 = self.__backtracking__(D2[:,:end_index], B2[:,:end_index], s2, t2[:end_index])
            alignment2 = alignment2[0][::-1], alignment2[1][::-1]
        else:
            alignment2 = self.__align_hirschberg__(s[delim:], t[min_index:])

        alignment = alignment1[0] + alignment2[0], alignment1[1] + alignment2[1]

        return alignment

    def __generate_matrix__(self, s: str, t: str):
        """
        Generates the score and backtracking matrices for the given strings.
        """
        n = len(s)
        m = len(t)

        D = np.zeros((n+1, m+1), dtype=int) # Distance matrix
        B = np.zeros((n+1, m+1), dtype=self.Direction) # Backtracking matrix

        B[0, 0] = self.Direction.NONE

        # Initialize first row and column
        for i in range(1, n+1):
            D[i, 0] =  D[i-1, 0] + self.w[s[i-1]]['-'] if self.type == self.AlignmentType.GLOBAL else 0
            B[i, 0] = self.Direction.UP if self.type == self.AlignmentType.GLOBAL else self.Direction.NONE

        for j in range(1, m+1):
            D[0, j] = D[0, j-1] + self.w['-'][t[j-1]] if self.type == self.AlignmentType.GLOBAL else 0
            B[0, j] = self.Direction.LEFT if self.type == self.AlignmentType.GLOBAL else self.Direction.NONE

        # Fill the matrices
        for i in range(1, n+1):
            for j in range(1, m+1):
                # Compute scores
                up_score = D[i-1, j] + self.w[s[i-1]]['-']
                left_score = D[i, j-1] + self.w['-'][t[j-1]]
                diag_score = D[i-1, j-1] + self.w[s[i-1]][t[j-1]]

                comparator = max if self.is_similarity else min

                best_score = comparator(up_score, left_score, diag_score)

                # Set the backtracking matrix
                if best_score < 0 and self.type == self.AlignmentType.LOCAL:
                    D[i, j] = 0
                    B[i, j] = self.Direction.NONE
                else:
                    D[i, j] = best_score
                    if best_score == left_score:
                        B[i, j] = self.Direction.LEFT
                    elif best_score == diag_score:
                        B[i, j] = self.Direction.DIAG
                    elif best_score == up_score:
                        B[i, j] = self.Direction.UP

        return D, B

    def __str__(self):
        result = ""

        if not self.hirschberg:
            arrow_left = '\u2190'
            arrow_up = '\u2191'
            arrow_diag = '\u2196'

            n = len(self.s)
            m = len(self.t)

            sep = "\t"

            output = sep

            for j in range(m):
                output += sep + self.t[j] + sep
        
            output += '\n'

            for i in range(2*n + 1):
                index_line = i // 2
                if i % 2 == 0:
                    output += sep

                    for j in range(m+1):
                        output += str(self.D[index_line, j]) + sep

                        if j < m:
                            output += (arrow_left if self.B[index_line, j+1] == self.Direction.LEFT else "") + sep
                else:
                    output += self.s[index_line] + sep

                    for j in range(m+1):              
                        output += (arrow_up if index_line < n and self.B[index_line+1, j] == self.Direction.UP else "") + sep
                        output += (arrow_diag if index_line < n and j < m and self.B[index_line+1, j+1] == self.Direction.DIAG else "") + sep
                
                output += '\n'

            tabsize = len(str(self.D.max())) + 1

            result += "Matrix:\n" + output.expandtabs(tabsize) + "\n"

        result += "Alignment:\n" + self.alignment[0] + "\n" + self.alignment[1] + "\n"
        return result

    def __backtracking__(self, D: np.ndarray, B: np.ndarray, s: str, t: str):
        """
        Performs backtracking on the given matrices and returns the alignment.
        """
        if self.type == self.AlignmentType.LOCAL:
            i, j = np.unravel_index(D.argmax(), D.shape)
        elif self.type == self.AlignmentType.GLOBAL:
            i, j = D.shape[0]-1, D.shape[1]-1
        else:
            raise ValueError("Invalid alignment type")

        s_aligned = ""
        t_aligned = ""

        while B[i, j] != Alignment.Direction.NONE and (self.type == self.AlignmentType.GLOBAL or D[i, j] > 0):
            if B[i, j] == Alignment.Direction.LEFT:
                s_aligned = '-' + s_aligned
                t_aligned = t[j-1] + t_aligned
                j -= 1
            elif B[i, j] == Alignment.Direction.UP:
                s_aligned = s[i-1] + s_aligned
                t_aligned = '-' + t_aligned
                i -= 1
            else:
                s_aligned = s[i-1] + s_aligned
                t_aligned = t[j-1] + t_aligned
                i -= 1
                j -= 1

        return s_aligned, t_aligned
