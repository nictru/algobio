#!/usr/bin/env python3

from typing import List, Set
from borders import actual_border

verbose = True

def log(msg: str):
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

def compute_extended_bad_character_table(pattern: str):
    """
    Compute the extended bad character table for the Boyer-Moore algorithm.
    """
    m = len(pattern)
    alphabet = set(pattern)

    return [compute_bad_character_table(pattern[:j], alphabet) for j in range(m + 1)]

def compute_shift_table(pattern: str):
    """
    Compute the shift table for the Boyer-Moore algorithm.
    """
    m = len(pattern)

    S: List[int] = [m] * m

    # Part 1: Sigma <= j
    border2: List[int] = [-1, 0]
    i = 0

    log("Part 1")
    # For all suffix start positions
    for j in range(2, m + 1):
        while i >= 0 and pattern[m-i-1] != pattern[m-j]:
            sigma = j - i - 1
            log(f"Iteration: i = {i}, j = {j}, sigma = {sigma}")

            if sigma < S[m-i-1]:
                log(f"Set S[{m-i-1}] to {sigma} (because {sigma} < {S[m-i-1]}))")
                S[m-i-1] = sigma
            else:
                log(f"Did not set S[{m-i-1}] to {sigma} (because {sigma} >= {S[m-i-1]}))")

            log(f"Set i to border2[{i}] = {border2[i]}")
            i = border2[i]
        
        if i < 0:
            log("Left while loop because i < 0")
        else:
            log("Left while loop because pattern[m-i-1] == pattern[m-j]")

        i += 1
        log(f"Incremented i to {i}")
        border2.append(i)
        log(f"Set border2[{j}] to {i}")

    log(f"Result after part 1: {S}")

    log("")

    log("Part 2")
    # Part 2: Sigma > j
    j = 0
    i = border2[m]
    while i >= 0:
        sigma = m-i
        log(f"Iteration: i = {i}, j = {j}, sigma = {sigma}")

        while j < sigma:
            if S[j] > sigma:
                log(f"Set S[{j}] to {sigma} (because {sigma} < {S[j]}))")
                S[j] = sigma
            else:
                log(f"Did not set S[{j}] to {sigma} (because {sigma} >= {S[j]}))")
            j += 1
        
        i = border2[i]

    log("Finished calculating shift table")

    return S

def boyer_moore_gs(text: str, pattern: str) -> bool:
    """
    Search for a pattern in a text using the Boyer-Moore algorithm.
    """
    n = len(text)
    m = len(pattern)

    log("Computing shift table")

    S = compute_shift_table(pattern)

    i = 0
    j = m - 1

    log(f"Initial values: i = {i}, j = {j}")

    while i <= n - m:
        log(f"Outer loop, i = {i}")
        while text[i+j] == pattern[j]:
            log(f"Inner loop, j = {j}")
            if j == 0:
                return True
            j -= 1
        i += S[j]
        j = m - 1

    return False

def boyer_moore_galil(text: str, pattern: str) -> bool:
    """
    Search for a pattern in a text using the Boyer-Moore-Galil algorithm.
    """
    n = len(text)
    m = len(pattern)

    log("Computing shift table")

    S = compute_shift_table(pattern)

    log("")

    i = 0
    j = m - 1
    start = 0
    Border = len(actual_border(pattern))

    log(f"Initial values: i = {i}, j = {j}, start = {start}, Border = {Border}")

    while i <= n - m:
        log(f"Outer loop, i = {i}")
        while text[i+j] == pattern[j]:
            log(f"Inner loop, j = {j}")
            if j == start:
                return True
            j -= 1

        if j == start:
            log(f"j == start, setting start to {Border}")
            start = Border
        else:
            log(f"j != start, setting start to {0}")
            start = 0

        i += S[j]
        j = m - 1

    return False

def boyer_moore_bc(text: str, pattern: str) -> bool:
    """
    Search for a pattern in a text using the Boyer-Moore algorithm with bad character rule.
    """
    n = len(text)
    m = len(pattern)

    i = 0
    j = m-1

    log("Computing bad character table")
    ebc = compute_extended_bad_character_table(pattern)
    log(f"Bad character table: {ebc}")

    while i <= n - m:
        log(f"Outer loop, i = {i}")
        while text[i+j] == pattern[j]:
            log(f"Inner loop, j = {j}")
            if j == 0:
                return True
            j -= 1
        
        log(f"Incrementing i by {j - ebc[j][text[i+j]]} (because ebc[{j}][{text[i+j]}] = {ebc[j][text[i+j]]} and j = {j})")
        i += j - ebc[j][text[i+j]]
        j = m - 1

    return False

if __name__ == "__main__":
    print("Found") if boyer_moore_bc("sdofjaababbababaaösldfkj", "ababbaba") else print("Not found")

