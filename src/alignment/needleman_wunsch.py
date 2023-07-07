#!/usr/bin/env python3

import numpy as np
from typing import Dict

LEFT = 5
DIAG = 6
UP = 7

def generate_matrix(s: str, t: str, w: Dict[str, Dict[str, int]]):
    n = len(s)
    m = len(t)

    D = np.zeros((n+1, m+1), dtype=int) # Distance matrix
    B = np.zeros((n+1, m+1), dtype=int) # Backtracking matrix

    # Initialize first row and column
    for i in range(1, n+1):
        D[i, 0] =  D[i-1, 0] + w[s[i-1]]['-']
        B[i, 0] = UP

    for j in range(1, m+1):
        D[0, j] = D[0, j-1] + w['-'][t[j-1]]
        B[0, j] = LEFT

    # Fill the matrices
    for i in range(1, n+1):
        for j in range(1, m+1):
            # Compute scores
            up_score = D[i-1, j] + w[s[i-1]]['-']
            left_score = D[i, j-1] + w['-'][t[j-1]]
            diag_score = D[i-1, j-1] + w[s[i-1]][t[j-1]]

            # Choose the minimum
            min_score = min(left_score, up_score, diag_score)

            D[i, j] = min_score

            # Set the backtracking matrix
            if min_score == left_score:
                B[i, j] = LEFT
            elif min_score == diag_score:
                B[i, j] = DIAG
            elif min_score == up_score:
                B[i, j] = UP

    return D, B

def pretty_print_matrix(D: np.ndarray, B: np.ndarray, s: str, t: str):
    arrow_left = '\u2190'
    arrow_up = '\u2191'
    arrow_diag = '\u2196'

    n = len(s)
    m = len(t)


    sep = "\t"

    output = sep

    for j in range(m):
        output += sep + t[j] + sep
   
    output += '\n'

    for i in range(2*n + 1):
        index_line = i // 2
        if i % 2 == 0:
            output += sep

            for j in range(m+1):
                output += str(D[index_line, j]) + sep

                if j < m:
                    output += (arrow_left if B[index_line, j+1] == LEFT else "") + sep
        else:
            output += s[index_line] + sep

            for j in range(m+1):              
                output += (arrow_up if index_line < n and B[index_line+1, j] == UP else "") + sep
                output += (arrow_diag if index_line < n and j < m and B[index_line+1, j+1] == DIAG else "") + sep
        
        output += '\n'

    tabsize = len(str(D.max())) + 1

    print(output.expandtabs(tabsize))


def backtracking(B: np.ndarray, s: str, t: str):
    n = B.shape[0] - 1
    m = B.shape[1] - 1

    i = n
    j = m

    s_aligned = ""
    t_aligned = ""

    while i > 0 or j > 0:
        if B[i, j] == LEFT:
            s_aligned = '-' + s_aligned
            t_aligned = t[j-1] + t_aligned
            j -= 1
        elif B[i, j] == UP:
            s_aligned = s[i-1] + s_aligned
            t_aligned = '-' + t_aligned
            i -= 1
        else:
            s_aligned = s[i-1] + s_aligned
            t_aligned = t[j-1] + t_aligned
            i -= 1
            j -= 1

    return s_aligned, t_aligned

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Needleman-Wunsch algorithm')
    parser.add_argument(type=str, dest="s", help='First sequence')
    parser.add_argument(type=str, dest="t", help='Second sequence')

    parser.add_argument('--match', type=int, default=0, help='Match score')
    parser.add_argument('--indel', type=int, default=2, help='Indel score')
    parser.add_argument('--substitution', type=int, default=3, help='Substitution score')

    args = parser.parse_args()

    s = args.s
    t = args.t

    alphabet = set(s + t)

    w = {
        a: {b: args.match if a == b else args.substitution for b in alphabet} for a in alphabet
    }

    w['-'] = {a: args.indel for a in alphabet}

    for a in alphabet:
        w[a]['-'] = args.indel

    D, B = generate_matrix(s, t, w)
    
    pretty_print_matrix(D, B, s, t)

    s_aligned, t_aligned = backtracking(B, s, t)
    print("s:", s_aligned)
    print("t:", t_aligned)