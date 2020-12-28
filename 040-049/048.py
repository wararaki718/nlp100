from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Morph:
    surface: str
    base: str
    pos: str
    pos1: str


@dataclass
class Chunk:
    dst: str # 係り先
    srcs: List[str] # 係り元
    morphs: List[Morph]

    @property
    def norm_surface(self) -> str:
        return ''.join(map(lambda x: x.surface, filter(lambda x: x.pos != '記号', self.morphs)))


class Loader:
    def __init__(self, filename: str):
        self._filename = filename

    def __iter__(self) -> List[Morph]:
        with open(self._filename, 'rt') as f:
            chunks = []
            chunk = None
            for line in f:
                sentence = line.strip()
                if sentence[0] == '*':
                    if chunk is not None:
                        chunks.append(chunk)
                    items = sentence.split()
                    chunk = Chunk(dst=items[1], srcs=[items[2].replace('D', '')], morphs=[])
                elif sentence == 'EOS':
                    if chunk is not None:
                        chunks.append(chunk)
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


def is_phrase(chunk: Chunk) -> bool:
    for morph in chunk.morphs:
        if morph.pos == '名詞':
            return True
    return False


def dfs(index: int, chunks: List[Chunk]) -> List[Chunk]:
    target_chunk = chunks[index]
    if '-1' in target_chunk.srcs:
        return [target_chunk]

    next_index = int(target_chunk.srcs[0])
    return [target_chunk] + dfs(next_index, chunks)


def show(chunks: List[Chunk]):
    results = []
    for chunk in chunks:
        result = ''.join(map(lambda morph: morph.surface, chunk.morphs))
        results.append(result)
    print(' -> '.join(results))


def main():
    # loader = Loader('ai.ja.txt.parsed')
    loader = Loader('sample.txt.parsed')
    sentence_chunks = []
    for chunks in loader:
        if chunks == []:
            continue
        sentence_chunks.append(chunks)

    # print(sentence_chunks)
    # print()
    for chunks in sentence_chunks:
        for i, chunk in enumerate(chunks):
            if not is_phrase(chunk):
                continue
            results = dfs(i, chunks)
            show(results)
    print('DONE')


if __name__ == '__main__':
    main()
