from typing import Dict


class Loader:
    def __init__(self, filename: str):
        self._filename = filename
    
    def __iter__(self) -> Dict[str, str]:
        with open(self._filename, 'rt') as f:
            sentences = []
            for line in f:
                if line.startswith('EOS'):
                    break
                items = line.split('\t')
                ma = items[1].split(',')
                sentence = {
                    'surface': items[0],
                    'base': ma[6],
                    'pos': ma[0],
                    'pos1': ma[1]
                }
                sentences.append(sentence)
                if items[0] == '。':
                    yield sentences
                    sentences = []

            if sentences != []:
                yield sentences


def main():
    loader = Loader('neko.txt.mecab')

    for sentences in loader:
        for sentence in sentences:
            if sentence['pos'] == '動詞':
                print(sentence['base'])
    print('DONE')


if __name__ == '__main__':
    main()
