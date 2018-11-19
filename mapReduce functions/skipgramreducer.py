#!/usr/bin/python

import sys

# Since the words are sorted, we know we have reached another word
# if the next one is not equal to previous.
# Basically repeating the process of our other reducers..
previous = None # Starts off with a null reducer since we don't have a point of comparison yet.
sum = 0 # A variable to keep track of how many previous items we've seen.
for line in sys.stdin:
    key, value = line.split("\t") # Splits the output of the mapper based of the tab value.
    if (key != previous): # If the phrase we're assessing is not the same as the previous...
        if previous is not None: # And is not null...
            print(previous+ '\t' + str(sum)) # Then we print the final accumilated sum with it's phrase.
        previous = key # Add the new phrase as the previous variable so we can start keeping tabs on it.
        sum = 0 # Reset the counter!
    sum = sum + int(value) # Increments the sum based on the tabulated value from the input.

print(previous+ '\t' + str(sum)) # For the very last value, we have to print it to the file seperately.

