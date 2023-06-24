#!/usr/bin/env python3

from typing import List, Set
from borders import actual_border

def log(msg: str, verbose: bool = False):
    if verbose:
        print(msg)

def compute_bad_character_table(pattern: str, alphabet: Set[str] | None = None):
    """
    Compute the bad character table for the Boyer-Moore algorithm.
    """
    m = len(pattern)
    
    if alphabet is None:
        alphabet = set(pattern)

    return {letter: max([k for k in range(-1, m) if k == -1 or pattern[k] == letter]) for letter in alphabet}

def compute_extended_bad_character_table(pattern: str, alphabet: Set[str] | None = None):
    """
    Compute the extended bad character table for the Boyer-Moore algorithm.
    """
    m = len(pattern)

    return [compute_bad_character_table(pattern[:j], alphabet) for j in range(m + 1)]

def compute_shift_table(pattern: str, verbose: bool = False):
    """
    Compute the shift table for the Boyer-Moore algorithm.
    """
    m = len(pattern)

    S: List[int] = [m] * m

    # Part 1: Sigma <= j
    border2: List[int] = [-1, 0]
    i = 0

    log("Part 1", verbose)
    # For all suffix start positions
    for j in range(2, m + 1):
        while i >= 0 and pattern[m-i-1] != pattern[m-j]:
            sigma = j - i - 1
            log(f"Iteration: i = {i}, j = {j}, sigma = {sigma}", verbose)

            if sigma < S[m-i-1]:
                log(f"Set S[{m-i-1}] to {sigma} (because {sigma} < {S[m-i-1]}))", verbose)
                S[m-i-1] = sigma
            else:
                log(f"Did not set S[{m-i-1}] to {sigma} (because {sigma} >= {S[m-i-1]}))", verbose)

            log(f"Set i to border2[{i}] = {border2[i]}")
            i = border2[i]
        
        if i < 0:
            log("Left while loop because i < 0", verbose)
        else:
            log("Left while loop because pattern[m-i-1] == pattern[m-j]", verbose)

        i += 1
        log(f"Incremented i to {i}", verbose)
        border2.append(i)
        log(f"Set border2[{j}] to {i}", verbose)

    log(f"Result after part 1: {S}", verbose)

    log("", verbose)

    log("Part 2", verbose)
    # Part 2: Sigma > j
    j = 0
    i = border2[m]
    while i >= 0:
        sigma = m-i
        log(f"Iteration: i = {i}, j = {j}, sigma = {sigma}", verbose)

        while j < sigma:
            if S[j] > sigma:
                log(f"Set S[{j}] to {sigma} (because {sigma} < {S[j]}))", verbose)
                S[j] = sigma
            else:
                log(f"Did not set S[{j}] to {sigma} (because {sigma} >= {S[j]}))", verbose)
            j += 1
        
        i = border2[i]

    log("Finished calculating shift table", verbose)

    return S

def boyer_moore_gs(text: str, pattern: str, verbose: bool = False) -> bool:
    """
    Search for a pattern in a text using the Boyer-Moore algorithm.
    """
    n = len(text)
    m = len(pattern)

    log("Computing shift table", verbose)

    S = compute_shift_table(pattern, verbose)

    i = 0
    j = m - 1

    log(f"Initial values: i = {i}, j = {j}", verbose)

    while i <= n - m:
        log(f"Outer loop, i = {i}", verbose)
        while text[i+j] == pattern[j]:
            log(f"Inner loop, j = {j}", verbose)
            if j == 0:
                return True
            j -= 1
        i += S[j]
        j = m - 1

    return False

def boyer_moore_galil(text: str, pattern: str, verbose: bool = False) -> bool:
    """
    Search for a pattern in a text using the Boyer-Moore-Galil algorithm.
    """
    n = len(text)
    m = len(pattern)

    log("Computing shift table", verbose)

    S = compute_shift_table(pattern, verbose)

    log("", verbose)

    i = 0
    j = m - 1
    start = 0
    Border = len(actual_border(pattern))

    log(f"Initial values: i = {i}, j = {j}, start = {start}, Border = {Border}", verbose)

    while i <= n - m:
        log(f"Outer loop, i = {i}", verbose)
        while text[i+j] == pattern[j]:
            log(f"Inner loop, j = {j}", verbose)
            if j == start:
                return True
            j -= 1

        if j == start:
            log(f"j == start, setting start to {Border}", verbose)
            start = Border
        else:
            log(f"j != start, setting start to {0}", verbose)
            start = 0

        i += S[j]
        j = m - 1

    return False

def boyer_moore_bc(text: str, pattern: str, verbose: bool = False) -> bool:
    """
    Search for a pattern in a text using the Boyer-Moore algorithm with bad character rule.
    """
    n = len(text)
    m = len(pattern)
    alphabet = set(pattern) | set(text)

    i = 0
    j = m-1

    log("Computing bad character table", verbose)
    ebc = compute_extended_bad_character_table(pattern)
    log(f"Bad character table: {ebc}", verbose)

    while i <= n - m:
        log(f"Outer loop, i = {i}", verbose)
        while text[i+j] == pattern[j]:
            log(f"Inner loop, j = {j}", verbose)
            if j == 0:
                return True
            j -= 1
        
        log(f"Incrementing i by {j - ebc[j][text[i+j]]} (because ebc[{j}][{text[i+j]}] = {ebc[j][text[i+j]]} and j = {j})", verbose)
        i += j - ebc[j][text[i+j]]
        j = m - 1

    return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search for a pattern in a text using the Boyer-Moore algorithm.")
    parser.add_argument("text", help="The text to search in")
    parser.add_argument("pattern", help="The pattern to search for")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print debug output")
    parser.add_argument("-a", "--algorithm", choices=["gs", "galil", "bc"], default="gs", help="The algorithm to use")

    args = parser.parse_args()
    
    if args.algorithm == "gs":
        algorithm = boyer_moore_gs
    elif args.algorithm == "galil":
        algorithm = boyer_moore_galil
    elif args.algorithm == "bc":
        algorithm = boyer_moore_bc
    
    print("Found") if algorithm(args.text, args.pattern, args.verbose) else print("Not found")

