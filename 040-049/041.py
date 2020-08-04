from dataclasses import dataclass
from typing import List

@dataclass
class Morph:
    surface: str
    base: str
    pos: str
    pos1: str


@dataclass
class Chunk:
    dst: str
    srcs: List[str]
    morphs: List[Morph]


class Loader:
    def __init__(self, filename: str):
        self._filename = filename

    def __iter__(self) -> List[Morph]:
        with open(self._filename, 'rt') as f:
            morphs = []
            chunks = []
            chunk = None
            for line in f:
                sentence = line.strip()
                if sentence[0] == '*':
                    if chunk is not None:
                        chunks.append(chunk)
                    items = sentence.split()
                    chunk = Chunk(dst=items[1], srcs=[items[2]], morphs=[])
                elif sentence == 'EOS':
                    yield chunks
                    chunks = []
                else:
                    items = sentence.split('\t')
                    results = items[1].split(',')
                    morph = Morph(
                        surface=items[0],
                        base=results[6],
                        pos=results[0],
                        pos1=results[1]
                    )
                    chunk.morphs.append(morph)


def main():
    loader = Loader('ai.ja.txt.parsed')
    sentence_chunks = []
    for chunk in loader:
        sentence_chunks.append(chunk)
    
    for chunk in sentence_chunks[1]:
        print(chunk)
    print('DONE')


if __name__ == '__main__':
    main()
