from collections import defaultdict
import string

import pandas as pd
from sklearn.model_selection import train_test_split


def show(df: pd.DataFrame):
    print(df.shape)
    print(df.publisher.value_counts())
    print()

def create_word2id_map(df: pd.DataFrame):
    word_counter = defaultdict(int)
    for title in df.title:
        for p in list(string.punctuation):
            title = title.replace(p, '')
        words = title.lower().split()
        for word in words:
            word_counter[word] += 1
    
    df = pd.DataFrame(word_counter.items(), columns=['word', 'total'])
    df = df[df.total > 1]
    df.sort_values('total', ascending=False, inplace=True)
    df.drop('total', axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'id'}, inplace=True)
    df['id'] = df.id + 1
    return df


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

    train_df.to_csv('data/train.txt', sep='\t', index=None)
    valid_df.to_csv('data/valid.txt', sep='\t', index=None)
    test_df.to_csv('data/test.txt', sep='\t', index=None)

    mapping_df = create_word2id_map(train_df)
    print(mapping_df.head(10))
    mapping_df.to_csv('data/mapping.csv', index=None)
    print('DONE')

    return 0


if __name__ == '__main__':
    main()
