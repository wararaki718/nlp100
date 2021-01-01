import pickle

import gensim
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def vectorize(df: pd.DataFrame, model: gensim.models.KeyedVectors) -> tuple:
    wordset = df.title.apply(lambda x: x.replace('.', '').replace(',', '').replace('!', '').replace('?', '').split())
    vectors = []
    for words in tqdm(wordset):
        tmp = []
        for word in words:
            if word in model.wv:
                tmp.append(model.wv[word])
        vector = np.array(tmp)
        vectors.append(vector.mean(0).tolist())
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

    (X, y) = vectorize(df, model)
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
