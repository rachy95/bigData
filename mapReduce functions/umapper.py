#!/usr/bin/python
import sys

# this is run with lyrics without stopwords or 1-length words
# we spit out each word with 1 to process later
for line in sys.stdin:
        for word in line.split():
                print(word + '\t1')
