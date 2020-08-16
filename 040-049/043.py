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
    dst: str # 係り先
    srcs: List[str] # 係り元
    morphs: List[Morph]


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


def is_valid_pos(morphs: List[str], target_pos: str) -> bool:
    for morph in morphs:
        if morph.pos == target_pos:
            return True
    return False


def get_bases(morphs: List[str]) -> List[str]:
    bases = []
    for morph in morphs:
        if morph.pos == '記号':
            continue
        bases.append(morph.base)
    return bases


def get_strs(target_dst: str, chunks: List[Chunk]) -> List[str]:
    bases = []
    for chunk in chunks:
        if target_dst == chunk.dst and not is_valid_pos(chunk.morphs, '動詞'):
            bases = get_bases(chunk.morphs)
            break
    return bases


def show(dst: str, bases: List[str]):
    text = "\t".join(bases)
    print(f'{dst}\t:\t{text}')


def main():
    loader = Loader('ai.ja.txt.parsed')
    sentence_chunks = []
    for sentence_chunk in loader:
        if sentence_chunk == []:
            continue
        sentence_chunks.append(sentence_chunk)
    
    for chunks in sentence_chunks:
        for chunk in chunks:
            base = get_bases(chunk.morphs)
            if base == [] and not is_valid_pos(chunk.morphs, '名詞'):
                continue
            t = "\t".join(base)
            for src in chunk.srcs:
                tmp = get_strs(src[:-1], chunks)
                if tmp != []:
                    show(t, tmp)
    print('DONE')


if __name__ == '__main__':
    main()
