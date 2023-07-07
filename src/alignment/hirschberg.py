#!/usr/bin/env python3

from typing import Dict
from needleman_wunsch import NeedlemanWunsch, main

class Hirschberg(NeedlemanWunsch):
    def __generate_matrix__(self, s: str, t: str, w: Dict[str, Dict[str, int]]):

        n = len(s)
        m = len(t)

        D = [0]

        for j in range(1, m+1):
            D.append(D[j-1] + w['-'][t[j-1]])

        for i in range(1, n+1):
            D_prev = D.copy()

            D[0] = D_prev[0] + w[s[i-1]]['-']

            for j in range(1, m+1):
                up_score = D_prev[j] + w[s[i-1]]['-']
                left_score = D[j-1] + w['-'][t[j-1]]
                diag_score = D_prev[j-1] + w[s[i-1]][t[j-1]]

                D[j] = min(up_score, left_score, diag_score)

        return D, None

if __name__ == '__main__':
    res = main("Hirschberg algorithm", Hirschberg)

    print(res.D)