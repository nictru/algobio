#!/usr/bin/env python3

from z_boxes import z_boxes
from typing import Callable, List

def compute_shift_table(word: str) -> list[int]:
    """
    Computes the border lengths of a word.
    """

    S = [-1, 0]

    i = 0

    for j in range(1, len(word)):
        while i >= 0 and word[i] != word[j]:
            i = S[i]
        i += 1
        S.append(i)

    return S

def compute_shift_table_z(word: str) -> list[int]:
    m = len(word)
    Z = z_boxes(word)
    S = [1]

    for j in range(1, m):
        S.append(j)
    
    sigma = m-1

    while sigma > 0:
        j = Z[sigma] + sigma
        S[j] = min(S[j], sigma)
        sigma -= 1
    
    return S

def kmp_general(text: str, word: str, shift_table_method: Callable[[str], List[int]] = compute_shift_table) -> bool:
    """
    Knuth-Morris-Pratt string search algorithm.
    """

    shift_table = shift_table_method(word)
    i = 0
    j = 0

    while i <= (len(text) - len(word)):
        while text[i + j] == word[j]:
            j += 1
            if (j >= len(word)):
                return True
        i = i+j-shift_table[j]
        j = max(0, shift_table[j])

    return False

def kmp(text: str, word: str) -> bool:
    return kmp_general(text, word, compute_shift_table)

def kmp_z(text: str, word: str) -> bool:
    return kmp_general(text, word, compute_shift_table_z)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aho-Corasick algorithm")
    parser.add_argument("--text", type=str, help="Text to search")
    parser.add_argument("--pattern", type=str, help="Pattern to search for")

    args = parser.parse_args()

    print("Found") if kmp(args.text, args.pattern) else print("Not found")