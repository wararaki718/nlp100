from dataclasses import dataclass
from typing import List, Optional


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


def make_path(chunks: List[Chunk],
              fix_first: Optional[str]=None,
              fix_last: Optional[str]=None):
    results = []
    if fix_first is not None:
        tmp = ''.join(map(lambda morph: morph.surface ,filter(lambda morph: morph.pos == '助詞', chunks[0].morphs)))
        results.append(f'{fix_first}{tmp}')
        chunks = chunks[1:]
    
    for chunk in chunks:
        result = ''.join(map(lambda morph: morph.surface, chunk.morphs))
        results.append(result)

    if fix_last is not None:
        tmp = ''.join(map(lambda morph: morph.surface ,filter(lambda morph: morph.pos == '助詞', chunks[-1].morphs)))
        results[-1] = f'{fix_first}{tmp}'

    text = ' -> '.join(results)
    return text


def show(i_chunks: List[Chunk], j_chunks: List[Chunk]):
    common_chunks = []
    n = min(len(i_chunks), len(j_chunks))
    for i in range(1, n+1):
        if not i_chunks[-i].dst == j_chunks[-i].dst:
            break
        common_chunks.append(i_chunks[-i])
    common_chunks = common_chunks[::-1]
    i_chunks = i_chunks[:-len(common_chunks)]
    j_chunks = j_chunks[:-len(common_chunks)]

    if len(j_chunks) > 0:
        result = ' | '.join(map(lambda x: make_path(x[0], x[1], x[2]), [(i_chunks, 'X', None), (j_chunks, 'Y', None), (common_chunks, None, None)]))
    else:
        result = make_path(i_chunks+[common_chunks[0]], 'X', 'Y')
    print(result)


def main():
    # loader = Loader('ai.ja.txt.parsed')
    loader = Loader('sample.txt.parsed')
    sentence_chunks = []
    for chunks in loader:
        if chunks == []:
            continue
        sentence_chunks.append(chunks)

    dependency_paths = []
    for chunks in sentence_chunks:
        for i, chunk in enumerate(chunks):
            if not is_phrase(chunk):
                continue
            results = dfs(i, chunks)
            dependency_paths.append(results)

    n = len(dependency_paths)
    for i in range(n-1):
        for j in range(i+1, n):
            show(dependency_paths[i], dependency_paths[j])

    print('DONE')


if __name__ == '__main__':
    main()
