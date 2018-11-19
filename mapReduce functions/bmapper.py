#!/usr/bin/python
import sys
# we run this python file with lyrics (which is lyrics with stopwords included)
# we decided on this because removing stop words could change the meaning of the
# phrase e.g. i don't like is not the same as like

# each line represents the lyrics of one song
for line in sys.stdin:
    # make each line an array of words
    words = line.split()
    for i in range(len(words)-1):
        # we pair together each word  with the next one
        # and stop at the word right before the end of the line
        bigram = words[i] + " "+ words[i+1]
        print(str(bigram) + "\t1")
