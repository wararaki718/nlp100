import string
from typing import List

import gensim
import pandas as pd


def sentence2words(sentence: str) -> List[str]:
    for p in list(string.punctuation):
        sentence = sentence.replace(p, '')
    words = sentence.lower().split()
    return words


class Word2IdConverter:
    def __init__(self, filename: str):
        df = pd.read_csv(filename)
        self._word2id_map = {row.word: row.id for row in df.itertuples()}
    
    def get_n_words(self) -> int:
        return len(self._word2id_map)

    def word2id(self, words: List[str]) -> List[int]:
        return list(map(lambda word: self._word2id_map[word] if word in self._word2id_map else 0, words))


class Word2VecIdConverter:
    def __init__(self, filename: str, modelname: str):
        df = pd.read_csv(filename)
        w2v = gensim.models.KeyedVectors.load_word2vec_format(modelname, binary=True)
        self._word2id_map = dict()
        for word in df.word:
            if word in w2v.vocab:
                self._word2id_map[word] = w2v.vocab[word].index
            else:
                self._word2id_map[word] = 0
        self._n_words = w2v.wv.syn0.shape[0]

    def get_n_words(self) -> int:
        return self._n_words

    def word2id(self, words: List[str]) -> List[int]:
        return list(map(lambda word: self._word2id_map[word] if word in self._word2id_map else 0, words))


if __name__ == '__main__':
    converter = Word2IdConverter('data/mapping.csv')
    w2v_converter = Word2VecIdConverter(
        'data/mapping.csv',
        'data/GoogleNews-vectors-negative300.bin'
    )
    words = 'to in the of for on'.split()
    ids = converter.word2id(words)
    print(ids)
    ids = w2v_converter.word2id(words)
    print(ids)
    print('')
    words = 'aaaaaaaaaa bbbbbbbbbbbbbbbbbbbb'.split()
    ids = converter.word2id(words)
    print(ids)
    ids = w2v_converter.word2id(words)
    print(ids)
    print('DONE')


    

