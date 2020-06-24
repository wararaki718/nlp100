import gzip
import json
import re


def main():
    data = []
    with gzip.open('jawiki-country.json.gz', 'rb') as f:
        for line in f:
            data.append(json.loads(line))
    
    for d in data:
        sentences = d['text'].split('\n')
        for sentence in sentences:
            result = re.findall(r'==+ (.+) ==+', sentence)
            if len(result) > 0:
                level = int(sentence.count('=')/2) - 1
                print(result[0], level)


if __name__ == '__main__':
    main()
