import gzip
import json


def main():
    data = []
    with gzip.open('jawiki-country.json.gz', 'rb') as f:
        for line in f:
            data.append(json.loads(line))
    
    for d in data:
        if 'イギリス' in d['title'] or 'イギリス' in d['text']:
            print(d['text'])

if __name__ == '__main__':
    main()
