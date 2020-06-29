import gzip
import json
import re


def main():
    data = []
    with gzip.open('jawiki-country.json.gz', 'rb') as f:
        for line in f:
            data.append(json.loads(line))
    
    results = []
    for d in data:
        sentences = d['text'].replace(' ', '').replace('"', '').split('\n')
        i = 0
        while len(sentences) > i:
            if not '基礎情報' in sentences[i]:
                i+=1
                continue
            
            i+=1
            result = dict()
            while len(sentences) > i and sentences[i] != '}}':
                items = sentences[i][1:].split('=')
                if len(items) < 2:
                    i+=1
                    continue
                result[items[0]] = items[1]
                i+=1
            results.append(result)
            break
    print(results[0])


if __name__ == '__main__':
    main()
