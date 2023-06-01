#!/usr/bin/env python3

def compute_border_lengths(word: str):
    """
    Computes the border lengths of a word.
    """

    border_lengths = [-1, 0]

    i = 0

    for j in range(1, len(word)):
        while i >= 0 and word[i] != word[j]:
            i = border_lengths[i]
        i += 1
        border_lengths.append(i)


    return border_lengths

def knuth_morris_pratt(text: str, word: str) -> bool:
    """
    Knuth-Morris-Pratt string search algorithm.
    """

    border_lengths = compute_border_lengths(word)
    i = 0
    j = 0

    while i <= (len(text) - len(word)):
        while text[i + j] == word[j]:
            j += 1
            if (j >= len(word)):
                return True
        i = i+j-border_lengths[j]
        j = max(0, border_lengths[j])

    return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aho-Corasick algorithm")
    parser.add_argument("--text", type=str, help="Text to search")
    parser.add_argument("--pattern", type=str, help="Pattern to search for")

    args = parser.parse_args()

    print("Found") if knuth_morris_pratt(args.text, args.pattern) else print("Not found")