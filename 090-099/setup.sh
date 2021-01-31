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
