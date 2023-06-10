def get_suffixes(word: str):
    return [word[i:] for i in range(len(word))][::-1]