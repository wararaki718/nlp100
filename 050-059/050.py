import pandas as pd
from sklearn.model_selection import train_test_split


def show(df: pd.DataFrame):
    print(df.shape)
    print(df.publisher.value_counts())
    print()


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
    print('DONE')

    return 0


if __name__ == '__main__':
    main()
