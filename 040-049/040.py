from dataclasses import dataclass

@dataclass
class Morph:
    surface: str
    base: str
    pos: str
    pos1: str


class Loader:
    def __init__(self, filename: str):
        self._filename = filename

    def __iter__(self) -> Morph:
        with open(self._filename, 'rt') as f:
            for line in f:
                if line[0] == '*':
                    continue
                items = line.split('\t')
                results = items[1].split(',')
                yield Morph(
                    surface=items[0],
                    base=results[6],
                    pos=results[0],
                    pos1=results[1]
                )
