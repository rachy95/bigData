#!/usr/bin/python
import sys

for line in sys.stdin:
    # make each line an array of words
    words = line.split()
    for i in range(len(words)-2):
        # we put 3 words that appear right beside each other together
        bigram = words[i] + " "+ words[i+1] + " " + words[i+2]
        print(str(bigram) + "\t1")
