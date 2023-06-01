#!/usr/bin/env python3

def naive(text: str, pattern: str) -> bool:
    """
    Naive string search algorithm
    """
    n = len(text)
    m = len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return True
    return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aho-Corasick algorithm")
    parser.add_argument("--text", type=str, help="Text to search")
    parser.add_argument("--pattern", type=str, help="Pattern to search for")

    args = parser.parse_args()

    print("Found") if naive(args.text, args.pattern) else print("Not found")