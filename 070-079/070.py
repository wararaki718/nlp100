import gc
import pickle

import gensim
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def vectorize(df: pd.DataFrame, model: gensim.models.KeyedVectors) -> tuple:
    vectors = []
    for title in tqdm(df.title):
        total = np.zeros(300)
        n = 0
        title = title.replace('.', '').replace(',', '').replace('!', '').replace('?', '')
        for word in title.split():
            if word in model.wv:
                total += model.wv[word]
        vectors.append((total/n).tolist())
    X = np.array(vectors)
    print(X.shape)

    label_map = {'b': 0, 't': 1, 'e': 2, 'm': 3}
    y = df.category.apply(lambda x: label_map[x]).values

    return (X, y)
    

def save(filename: str, data: tuple):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def main():
    model = gensim.models.KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)

    df = pd.read_csv('data/newsCorpora.csv', sep='\t', header=None)
    columns = [
        'id',
        'title',
        'url',
        'publisher',
        'category',
        'story',
        'hostname',
        'timestamp'
    ]
    df.columns = columns
    df.drop(['id', 'url', 'publisher', 'story', 'hostname', 'timestamp'], inplace=True)

    (X, y) = vectorize(df, model)
    del df
    del columns
    gc.collect()

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42, shuffle=True)
    X_valid, X_test, y_valid, y_test = train_test_split(X_test, y_test, train_size=0.5, random_state=42, shuffle=True)

    print(X_train.shape)
    print(X_test.shape)
    print(X_valid.shape)

    save('data/train.pkl', (X_train, y_train))
    save('data/valid.pkl', (X_valid, y_valid))
    save('data/test.pkl', (X_test, y_test))
    print('DONE')


if __name__ == '__main__':
    main()
