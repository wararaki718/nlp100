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
                value = re.search(r'\[\[(.+)\]\]', items[1])

                if value is not None:
                    value = value.group(1) \
                                .replace('[[', '') \
                                .replace(']]', '') \
                                .replace('<!--', '') \
                                .replace('-->', '') \
                                .replace('<refname', '') \
                                .replace('<small>', '') \
                                .replace('</small>', '')
                    if items[0] == '国章画像':
                        new_value = value.split(':')[1].split('|')[0]
                    elif value.startswith('[http'):
                        new_value = value.replace('[', '').replace(']', '').split('|')[0]
                    elif '#' in value:
                        new_value = value.split('#')[0]
                    elif '|' in value:
                        new_value = value.split('|')[0]
                    else:
                        new_value = value
                    result[items[0]] = new_value
                else:
                    new_value = re.sub(r'\[http:.+\]', '', items[1])
                    result[items[0]] = new_value \
                                        .replace('<refname', '') \
                                        .replace('<small>', '') \
                                        .replace('</small>', '') \
                                        .replace('<br/>', ' ') \
                                        .replace('<!--', '') \
                                        .replace('-->', '') \
                                        .replace('<references/>', '') \
                                        .replace('<ref>', '') \
                                        .replace('</ref>', '') \
                                        .replace('[[', '') \
                                        .replace(']]', '')
                i+=1
            results.append(result)
    print(results[0:5])


if __name__ == '__main__':
    main()
