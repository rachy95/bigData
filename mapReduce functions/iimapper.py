#!/usr/bin/python
import sys
# we run this file with the lyricsWithoutstopwords.txt 
# because we have cleaned out the stopwords in that file

# each line is a song lyric, so give each song an index
index = 0
for line in sys.stdin:
        for word in line.split():
                print(word + '\t' + str(index))
        
        # increment the index after we finish processing all the words in the lyrics
        # of that song
        index +=1
