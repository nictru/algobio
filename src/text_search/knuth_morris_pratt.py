#!/usr/bin/env python3

from z_boxes import z_boxes
from typing import Callable, List

def log(msg: str = "", verbose: bool = False):
    if verbose:
        print(msg)

def __compute_shift_table__(word: str) -> list[int]:
    """
    Computes the border lengths of a word.
    """
    m = len(word)
    S = [-1, 0]
    i = 0

    for j in range(2, m+1):
        while i >= 0 and word[i] != word[j-1]:
            i = S[i]
        i += 1
        S.append(i)

    return S

def __compute_shift_table_z__(word: str) -> list[int]:
    """
    Computes the border lengths of a word using the Z-algorithm.
    """
    m = len(word)
    Z = z_boxes(word)
    S = [-1, 0] # Made a slight adjustment here, otherwise the algorithm ends up in an infinite loop

    for j in range(2, m+1):
        S.append(j)
    
    sigma = m-1

    while sigma > 0:
        j = Z[sigma] + sigma
        S[j] = min(S[j], sigma)
        sigma -= 1
    
    return S

def __kmp_general__(text: str, pattern: str, shift_table_method: Callable[[str], List[int]] = __compute_shift_table__, verbose: bool = False) -> bool:
    """
    Knuth-Morris-Pratt string search algorithm.
    """

    m = len(pattern)
    n = len(text)

    log("Computing shift table...", verbose)
    shift_table = shift_table_method(pattern)
    log(f"Shift table: {shift_table}", verbose)

    i = 0
    j = 0

    while i <= (n - m):
        log(f"Outer loop, i = {i}, j = {j}", verbose)
        while text[i + j] == pattern[j]:
            log(f"Inner loop, i = {i}, j = {j}", verbose)
            j += 1
            if (j >= len(pattern)):
                return True
            
        log(f"Incrementing i by {j - shift_table[j]}", verbose)
        i += j - shift_table[j]
        j = max(0, shift_table[j])

        if shift_table[j] > 0:
            log(f"Setting j to shift_table[{j}]={shift_table[j]}", verbose)
            j = shift_table[j]
        else:
            log(f"Setting j to 0 because shift_table[{j}] = {shift_table[j]} <= 0", verbose)

    return False

def kmp(text: str, word: str, z: bool = False, verbose: bool = False) -> bool:
    return __kmp_general__(text, word, __compute_shift_table_z__ if z else __compute_shift_table__, verbose)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Knuth-Morris-Pratt algorithm")
    parser.add_argument("--text", type=str, help="Text to search")
    parser.add_argument("--pattern", type=str, help="Pattern to search for")
    parser.add_argument("-z", action="store_true", help="Use Z-boxes algorithm")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    print("Found") if kmp(args.text, args.pattern, args.z, args.verbose) else print("Not found")