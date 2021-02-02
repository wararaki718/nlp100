#!/bin/bash

mkdir data
cd data
wget http://www.phontron.com/kftt/download/kftt-data-1.0.tar.gz
tar xvzf kftt-data-1.0.tar.gz
rm kftt-data-1.0.tar.gz
cd ..

echo "DONE"
