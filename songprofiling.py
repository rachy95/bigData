import csv, os, sys, re, nltk, math, operator
from pprint import pprint
from nltk.corpus import stopwords
  

#artist,song,link,text
class songprofiling(object):
    songs = []
    all_words = {}

    # Initializes the class, opens the file and puts the values of rows into a global list called 'songs' 
    # in which they are stored in a dictionary format.
    def __init__(self):
        sys.stdin.readline()
        for songRow in csv.reader(iter(sys.stdin.readline, '')):
            song = {
             "title": songRow[1],
            "lyrics": songRow[3]
            }
            self.songs.append(song)

    #this is the same for each word
    def calculcateDocumentFrequency(self):
        all_words = {}
        #get that row of songs
        for song in self.songs:
            words = self.preProcessLyrics(song)
            #we only need the word to appear once so we check that specific word how many times
            #it appears in all the other documents
            words = set(words)
            for word in words:
                if word not in all_words:
                    all_words[word] = 1
                else:
                    all_words[word] += 1
                #print("song: " + song["title"] + " | df: " + str(all_words[word]))
        return all_words

    # this is different per song
    def calculateTermFrequency(self, song):
        word_frequency = {}
        words = self.preProcessLyrics(song)
        for word in words:
            if word not in word_frequency.keys():
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1
        return word_frequency

    def calculcatetfIdf(self, song):
        words_idf = self.calculcateDocumentFrequency()
        N = len(self.songs)
        all_words = {}
            
        words_tf = self.calculateTermFrequency(song)
        #get all the words frequency for that song
        for word in words_tf:
            #get that word and get the idf for that word
            idf = words_idf[word]
            idf = math.log10(N/idf)
            tf = 1+ math.log10(words_tf[word])
            tf_idf = tf * idf
            all_words[word] = tf_idf

        
        top_words = dict(sorted(all_words.items(), key=operator.itemgetter(1), reverse=True)[:50])
        return top_words

    def preProcessLyrics(self, song):
        lyrics = song["lyrics"]
        stop_words = set(stopwords.words('english')) 
        #get an array of all the words
        words = re.findall(r'\w+', lyrics)
        filtered_lyrics = []
        for word in words:
            word = word.lower()
            if word not in stop_words:
                filtered_lyrics.append(word)
        return filtered_lyrics


sp = songprofiling()
# for song in sp.songs:
song = sp.songs[0]
print(song["title"])
words_and_tf_idf = sp.calculcatetfIdf(song)
for word in words_and_tf_idf:
    print(word + ": " + str(words_and_tf_idf[word]))