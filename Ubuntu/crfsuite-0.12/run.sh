#! bin/bash

cd example
cat train.txt | ./chunking.py > train.crfsuite.txt
cat test.txt | ./chunking.py > test.crfsuite.txt
cd ..
bin/crfsuite learn -m zh_seg.model example/train.crfsuite.txt
bin/crfsuite tag -qt -m zh_seg.model example/test.crfsuite.txt