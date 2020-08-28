from dataclasses import dataclass
from typing import List, Dict

from graphviz import Digraph


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


def get_target_chunk(target_dst: str, chunks: List[Chunk]) -> Chunk:
    for chunk in chunks:
        if target_dst == chunk.dst:
            return chunk
    return None


def plot_tree(edges: List[Dict[str, Chunk]], filename: str):
    graph = Digraph(format='png')

    nodes = set()
    for edge in edges:
        nodes.add(edge['src'].norm_surface)
        nodes.add(edge['dst'].norm_surface)
    
    for node in nodes:
        graph.node(node)
    
    memos = []
    for edge in edges:
        src = edge['src'].norm_surface
        dst = edge['dst'].norm_surface
        tmp = f'{src}_{dst}'
        if tmp in memos:
            continue
        memos.append(tmp)
        graph.edge(src, dst)
    
    graph.render(filename)


def main():
    loader = Loader('ai.ja.txt.parsed')
    sentence_chunks = []
    for sentence_chunk in loader:
        if sentence_chunk == []:
            continue
        sentence_chunks.append(sentence_chunk)
    
    index = 1
    for chunks in sentence_chunks:
        edges = []
        for chunk in chunks:
            if chunk.dst == -1 or chunk.norm_surface == '':
                continue
            
            for src in chunk.srcs:
                dst_chunk = get_target_chunk(src, chunks)
                if dst_chunk is None or dst_chunk.norm_surface == '':
                    continue
                edges.append({'src': chunk, 'dst': dst_chunk})
        
        if len(edges) > 0:
            plot_tree(edges, f'images/tree_{index:04d}')
            index += 1
        
        if index == 5: # debug
            break

    print('DONE')


if __name__ == '__main__':
    main()
