import gzip
import json
import re

import requests


class WikiClient:
    def __init__(self, url: str='https://en.wikipedia.org/w/api.php'):
        self._url = url

    def get_image(self, title: str) -> dict:
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'imageinfo',
            'titles': title,
            'iiprop': 'url'
        }
        response = requests.get(url=self._url, params=params)
        return response.json()


def main():
    client = WikiClient()
    title = 'File:Billy_Tipton.jpg'

    data = []
    with gzip.open('jawiki-country.json.gz', 'rb') as f:
        for line in f:
            data.append(json.loads(line))
    
    for d in data:
        texts = d['text'].split('\n')
        for text in texts:
            if '国章画像' in text:
                title = text \
                            .replace('[', '') \
                            .replace(']', '') \
                            .replace(' ', '') \
                            .split('=')[1] \
                            .split('|')[0] \
                            .replace('ファイル', 'File') \
                            .replace('画像', 'File')
                result = client.get_image(title)

                try:
                    imageinfo = result.get('query').get('pages').get('-1').get('imageinfo')
                    print(imageinfo[0].get('url'))
                except:
                    print(f'{title} url is None')
    print('DONE')


if __name__ == '__main__':
    main()
