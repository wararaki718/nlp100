import gzip
import json


def main():
    data = []
    with gzip.open('jawiki-country.json.gz', 'rb') as f:
        for line in f:
            data.append(json.loads(line))
    
    for d in data:
        sentences = d['text'].split('\n')
        for sentence in sentences:
            if 'Category' in sentence:
                s = sentence.replace(']', '').replace('[', '').replace('{', '').replace('}', '')
                words = s.split('|')
                for word in words:
                    if 'Category' in word:
                        print(word.split(':')[-1])
                        break


if __name__ == '__main__':
    main()
