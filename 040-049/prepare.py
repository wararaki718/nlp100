import CaboCha


def main():
    parser = CaboCha.Parser()
    filenames = ['ai.ja.txt', 'sample.txt', 'sample2.txt']
    for filename in filenames:
        with open(filename, 'rt') as rf, open(f'{filename}.parsed', 'wt') as wf:
            for line in rf:
                if line == '\n':
                    continue
                parsed_text = parser.parse(line)
                wf.write(parsed_text.toString(CaboCha.FORMAT_LATTICE))
    print('DONE')


if __name__ == '__main__':
    main()
