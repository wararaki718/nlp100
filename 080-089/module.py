from typing import List

import pandas as pd

class Word2IdConverter:
    def __init__(self, filename: str):
        df = pd.read_csv(filename)
        self._word2id_map = {row.word: row.id for row in df.itertuples()}

    def word2id(self, words: List[str]) -> List[int]:
        return list(map(lambda word: self._word2id_map[word] if word in self._word2id_map else 0, words))


if __name__ == '__main__':
    converter = Word2IdConverter('data/mapping.csv')
    words = 'to in the of for on'.split()
    ids = converter.word2id(words)
    print(ids)
    words = 'aaaaaaaaaa bbbbbbbbbbbbbbbbbbbb'.split()
    ids = converter.word2id(words)
    print(ids)
    print('DONE')
