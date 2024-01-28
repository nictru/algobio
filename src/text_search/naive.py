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


def naive2(text: str, pattern: str) -> bool:
    """
    Naive string search algorithm, searching from right to left
    """
    n = len(text)
    m = len(pattern)

    for i in range(n - m + 1):
        j = m - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j == -1:
            return True

    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Aho-Corasick algorithm")
    parser.add_argument("--text", type=str, help="Text to search")
    parser.add_argument("--pattern", type=str, help="Pattern to search for")

    args = parser.parse_args()

    if not args.text or not args.pattern:
        parser.print_help()
        exit(1)

    print("Naive", end="\t")
    print("Found") if naive(args.text, args.pattern) else print("Not found")

    print("Naive2", end="\t")
    print("Found") if naive2(args.text, args.pattern) else print("Not found")


if __name__ == "__main__":
    main()
