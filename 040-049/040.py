from dataclasses import dataclass
from typing import List

@dataclass
class Morph:
    surface: str
    base: str
    pos: str
    pos1: str


class Loader:
    def __init__(self, filename: str):
        self._filename = filename

    def __iter__(self) -> List[Morph]:
        with open(self._filename, 'rt') as f:
            morphs = []
            for line in f:
                sentence = line.strip()
                if sentence[0] == '*':
                    continue
                if sentence == 'EOS':
                    yield morphs
                    morphs = []
                    continue
                items = sentence.split('\t')
                results = items[1].split(',')
                morph = Morph(
                    surface=items[0],
                    base=results[6],
                    pos=results[0],
                    pos1=results[1]
                )
                morphs.append(morph)


def main():
    loader = Loader('ai.ja.txt.parsed')
    sentence_morphs = []
    for morph in loader:
        sentence_morphs.append(morph)
    
    for morph in sentence_morphs[1]:
        print(morph)
    print('DONE')


if __name__ == '__main__':
    main()
