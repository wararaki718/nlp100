import gzip
import json
import re


def main():
    data = []
    with gzip.open('jawiki-country.json.gz', 'rb') as f:
        for line in f:
            data.append(json.loads(line))
    
    for d in data:
        sentences = d['text'].replace(' ', '').split('\n')
        for sentence in sentences:
            result = re.findall(r'\[\[File:(.+)', sentence)
            result += re.findall(r'\[\[ファイル:(.+)', sentence)
            if len(result) > 0:
                print(result[0].split('|')[0])


if __name__ == '__main__':
    main()
