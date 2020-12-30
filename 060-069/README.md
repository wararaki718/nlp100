# setup

## download w2v model

project page
- https://code.google.com/archive/p/word2vec/

download link
- https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit

after downloaded the model, you move the model from Donwloads directory to data directory.  
the command is below.

```shell
cd data
mv ~/Downloads/GoogleNews-vectors-negative300.bin.gz .
gzip -d GoogleNews-vectors-negative300.bin.gz
cd -
```

download evaluation dataset

```shell
cd data
wget http://download.tensorflow.org/data/questions-words.txt
cd -
```

```shell
cd data
mkdir wordsim
cd wordsim
wget http://www.gabrilovich.com/resources/data/wordsim353/wordsim353.zip
unzip wordsim353.zip
rm wordsim353.zip
cd ../..

```

## install libraries

```shell
pip install gensim tqdm scikit-learn pandas
```
