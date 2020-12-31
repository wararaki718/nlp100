from typing import Tuple

import pickle
import pandas as pd
from scipy.sparse import hstack, save_npz, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer


def show(df: pd.DataFrame):
    print(df.shape)
    print(df.publisher.value_counts())
    print()


def fit(df: pd.DataFrame) -> Tuple:
    hostname_encoder = OneHotEncoder(handle_unknown='ignore').fit(df.hostname.unique().reshape(-1, 1))
    publisher_encoder = OneHotEncoder(handle_unknown='ignore').fit(df.publisher.unique().reshape(-1, 1))
    title_vectorizer = TfidfVectorizer().fit(df.title)
    return (hostname_encoder, publisher_encoder, title_vectorizer)


def create_vectors(vectorizers: Tuple, df: pd.DataFrame) -> csr_matrix:
    vectors = hstack([
        vectorizers[2].transform(df.title),
        vectorizers[1].transform(df.publisher.values.reshape(-1, 1)),
        vectorizers[0].transform(df.hostname.values.reshape(-1, 1))
    ])

    label_map = {'b': 0, 't': 1, 'e': 2, 'm': 3}
    y = df.category.apply(lambda x: label_map[x]).values
    return vectors.tocsr(), y


def save_vectors(data: Tuple, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def main():
    filename = 'data/newsCorpora.csv'
    df = pd.read_csv(filename, sep='\t', header=None)
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
    print(df.shape)

    target_publishers = [
        'Reuters',
        'Huffington Post',
        'Businessweek',
        'Contactmusic.com',
        'Daily Mail'
    ]
    df = df[df.publisher.isin(target_publishers)]
    print(df.shape)
    print()

    train_df, test_df = train_test_split(df, train_size=0.8, random_state=42, shuffle=True)
    valid_df, test_df = train_test_split(test_df, train_size=0.5, random_state=42, shuffle=True)

    show(train_df)
    show(valid_df)
    show(test_df)

    # train_df.to_csv('data/train.txt', sep='\t', index=None)
    # valid_df.to_csv('data/valid.txt', sep='\t', index=None)
    # test_df.to_csv('data/test.txt', sep='\t', index=None)

    vectorizers = fit(train_df)

    train = create_vectors(vectorizers, train_df)
    valid = create_vectors(vectorizers, valid_df)
    test = create_vectors(vectorizers, test_df)

    save_vectors(train, 'data/train.pkl')
    save_vectors(valid, 'data/valid.pkl')
    save_vectors(test, 'data/test.pkl')


    print('DONE')

    return 0


if __name__ == '__main__':
    main()
