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

def knuth_morris_pratt(text: str, word: str):
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
                return i
        i = i+j-border_lengths[j]
        j = max(0, border_lengths[j])

    return -1

if __name__ == "__main__":
    print(knuth_morris_pratt("aabaabaac", "aabaac"))

    