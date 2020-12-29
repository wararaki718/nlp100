#!/bin/bash
mkdir data
cd data
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00359/NewsAggregatorDataset.zip
unzip NewsAggregatorDataset.zip
rm NewsAggregatorDataset.zip
cd -
