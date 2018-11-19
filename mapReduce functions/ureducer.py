#!/usr/bin/python
import sys

previous = None
count = 0

for line in sys.stdin:
    key, value = line.split('\t')
    # since the words are sorted, we know we have reached another word
    # if the next one is not equal to previous
    if key != previous:
        if previous is not None:
            print(previous + '\t' + str(count))
        previous = key
        count = 0

    count = count + int(value)

print(previous + '\t' + str(count))