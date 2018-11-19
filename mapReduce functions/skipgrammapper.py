#!/usr/bin/python
import sys, re

K = 1 # Preset by assignment specifications. The number of words to skip.
N = 2 # Preset by assignment specifications. The number of words to store.
temp = "" # Stores the word we are about to the print for the reducer.
for line in sys.stdin:
    words = line.split() # Splits each song's lyrics into an array of words.
    for index, value in enumerate(words): 
        # For every word in the array, we extract K-skip-N-grams.
        k = 0 # We start off skipping 0 words.
        temp = words[index] # We store the initial word.
        flag = 0 # Makes sure we do not have words of length != N.
        while k <= K: # For every skip variation...
            n = 1 # Starts off with one word added and keep going until we have N words.
            while n < N:
                if (index + n + k < len(words)): # It checks index+k+n to assess the nth word from the index whilst skipping k values.
                    flag = 1 # This means that we are maintaining N words.
                    temp = temp + " " +  words[index+n+k] + " " 
                else: 
                    flag = 0 # The temp length != N, so... we don't print it for the reducer.
                n = n + 1 
            k = k + 1 # we increment k so we know how many words to skip the next time
            if (flag == 1): # Only add it to the reducer if the flag is true!
                print(temp + "\t1")

            # now we reset the temp word, to continue on with k
            temp = words[index]