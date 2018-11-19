#!/usr/bin/python
import sys

previous = None
songIndexes = []

for line in sys.stdin:
    key, value = line.split('\t')

    # here we are not summing up the numbers
    # instead we are making the indexes an array so we know
    # all the songs that a word appears in
    if key != previous:
        if previous is not None:
            print(previous + '\t' + str(songIndexes))
        previous = key
        songIndexes = []

    # decision not to include duplicates, we are not trying to include
    # frequency of word in a song, but we are looking at how many times it appears in 
    # different songs
    if int(value) not in songIndexes:
        songIndexes.append(int(value))

print(previous + '\t' + str(songIndexes))
