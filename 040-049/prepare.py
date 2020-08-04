import CaboCha


def main():
    parser = CaboCha.Parser()
    
    with open('ai.ja.txt', 'rt') as rf, open('ai.ja.txt.parsed', 'wt') as wf:
        for line in rf:
            if line == '\n':
                continue
            parsed_text = parser.parse(line)
            wf.write(parsed_text.toString(CaboCha.FORMAT_LATTICE))
    print('DONE')


if __name__ == '__main__':
    main()
