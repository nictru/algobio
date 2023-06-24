from typing import List

def borders(word: str) -> List[str]:
    """
    Calculates all borders of a word.
    """

    borders = [""]

    for i in range(len(word)):
        substring = word[:i + 1]

        if substring == word[-len(substring):]:
            borders.append(substring)
    
    return borders

def real_borders(word: str) -> List[str]:
    """
    Finds the real borders of a word.
    """

    return [border for border in borders(word) if len(border) < len(word)]

def actual_border(word: str) -> str:
    """
    Finds the actual border of a word.
    """

    return max(real_borders(word), key=len)

if __name__ == "__main__":
    print(actual_border("aabaabaa"))
