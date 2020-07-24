import MeCab


def main():
    with open('neko.txt', 'rt') as f:
        text = f.read()
    
    tagger = MeCab.Tagger()
    result = tagger.parse(text)
    with open('neko.txt.mecab', 'wt') as f:
        f.write(result)
    print('DONE')


if __name__ == '__main__':
    main()
