#!/bin/bash

git clone https://github.com/moses-smt/giza-pp.git
cd giza-pp
make
cd ..
echo "setup GIZA++"

# minimal setup
git clone https://github.com/moses-smt/mosesdecoder.git
cd mosesdecoder
./bjam -j4
cd ..
echo "setup Moses"

echo "DONE"

wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz
tar xvzf kytea-0.4.7.tar.gz
cd kytea-0.4.7
./configure
make -j4
sudo ldconfig
cd ..
