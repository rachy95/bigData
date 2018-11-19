import re, os
import csv


lyricstxt = open("lyrics.txt", "w+")
lyricswithoutstopwords = open("lyricsWithoutStopWords.txt", "w+")

# stop words gotten by running stopwords.py to extract this from nltk's stopwords
stop_words = ["aa", "youd", 'our', 'won', 'both', 'it', 'been', 'then', "youll", 'werent', 'for', "havent", 's', 'couldnt',
              'this', 'theirs', 'if', 'your', 'not', 'me', 'they', 'above', 'any', 'ours', 'because', 'youre', 'his',
              'them', 'itself', 'there', 'those', 'arent', 'and', 'in', 'when', 'o', 'shouldnt', 'of', "didnt", 'her', 
              'just', 'what', "wouldnt", 'until', 'a', 'but', "hasnt", 'between', 'wouldnt', "thatll", 'with', 'yourselves', 
              'from', 'is', 'on', 'had', 'yourself', "shouldve", "neednt", 'such', 'out', 'during', 'to', 'having', 'has', 
              'other', 'by', 'mightnt', 'few', 'aint', 'or', 'does', 'nor', 'so', 'same', 'being', 'about', 'themselves', 
              'where', 'hasnt', 'shant', 'into', 'now', 'down', 'further', 'ma', 'do', 'have', 'as', 'some', 'herself', 
              'ourselves', 'can', 'up', "werent", "doesnt", 'am','at', "youve", 'hers', 'which', 'him', 'whom', 'through', 
              'no', 'while', 'its', 'each', 'doing', 'against', 'how', "wont", 'hadnt', 'was', 'that', 'more', 'most', 
              "isnt", 'who', "arent", 'be', 'only',"wasnt", 'all', 'under', 'before', 'wasnt', 'i', 'dont', 'she', 'over', "its", 
              'yours', 'were', 'he', 'too', 'these', 'off', 'again', "shant", "shouldnt", 'myself', 'than', 'doesnt', "mustnt", 'my', 
              'why', 'very', 'below', 'once', "dont", 'isnt', 'their', 'after', 'y', "you're", 'neednt', "shes", 'shouldve', 'own', 
              'are', 'mustnt', 'we', 'havent', 'the', 'will', 'did', 'you', "hadnt", 'an', 'himself', 'didnt', 'here', "mightnt"]


with open("songdata.csv", "r") as songData:
    songRows = csv.reader(songData)
    #remove the header
    next(songRows)
    for song in songRows:
        #get the lyrics
        lyrics = song[3]
        # we wanted one lyrics file without stopwords, to use for
        # indexing and for unigrams. Unigrams don't need stopwords.
        # also, we want another lyrics file with stopwords
        words = ""
        wordsWithoutStopWords = ""
        #clean up the lyrics
        for word in lyrics.split():
            word = word.lower()
            # remove numbers
            word = re.sub(r'[0-9]+', '', word)
            # remove non-words e.g , or '
            word = re.sub(r'[^\w\s]', '', word)
            # append word to words with a space, so all words in this particular
            # lyrics are separated by a space

            # we want to remove every single character except i, 
            # because 'I love' means something different than 'we love'
            # but characters like a or b ... do not mean much to us
            if len(word) > 1 or word=='i':
                words = words + " " + word

            # remove stop words or words that are of one character
            if word not in stop_words and len(word)>1:
                wordsWithoutStopWords = wordsWithoutStopWords + " " + word
        
        
        # each line contains the full lyrics for one song meaning
        # each song's lyrics is on a new line
        #--- remove leading and trailing whitespace---
        words = words.strip()
        wordsWithoutStopWords = wordsWithoutStopWords.strip()
        lyricstxt.write(words + "\n")
        lyricswithoutstopwords.write(wordsWithoutStopWords + "\n")
