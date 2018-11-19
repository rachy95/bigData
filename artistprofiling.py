import csv, os, sys, re, nltk, math, operator
from pprint import pprint
from nltk.corpus import stopwords
  

#artist,song,link,text
class artistprofiling(object):
    songsPerArtist = {}
    all_words = {}

    # Initializes the class, opens the file and puts the values of rows into a global list called 'songs' 
    # in which they are stored in a dictionary format.
    def __init__(self):
        data = csv.reader(iter(sys.stdin.readline, ''))
        next(data)
        for songRow in data:
            artist = songRow[0]
            lyrics = songRow[3]
            if artist not in self.songsPerArtist:
                self.songsPerArtist[artist] = lyrics
            else:   # We concatenate the lyrics of all the songs per artists into document.
                self.songsPerArtist[artist] += lyrics


    # the document has now become an artist with all the lyrics compiled together and so we calculat the document frequency and store it in a map.
    def calculcateDocumentFrequency(self):
        all_words = {}
        #get that row of lyrics
        for artist in self.songsPerArtist:
            lyrics = self.songsPerArtist[artist]
            words = self.preProcessLyrics(lyrics)
            #we only need the word to appear once so we check that specific word how many times
            #it appears in all the other documents
            words = set(words)
            for word in words:
                if word not in all_words:
                    all_words[word] = 1
                else:
                    all_words[word] += 1
        return all_words

    # Calculates the amount of times a term appears in all the songs of an artist. The lyrics that we pass are a concantenation of all the artists song lyrics.
    def calculateTermFrequency(self, lyrics):
        word_frequency = {}
        words = self.preProcessLyrics(lyrics)
        for word in words:
            if word not in word_frequency.keys():
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1
        return word_frequency

    # Uses the values from the document frequency and term frequency 
    def calculcatetfIdf(self, song):
        words_idf = self.calculcateDocumentFrequency()
        N = len(self.songsPerArtist)
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

        
        top_words = dict(sorted(all_words.items(), key=operator.itemgetter(1), reverse=True)[:100])
        return top_words

    # This method removes the stopwords, removes punctuation and sets the words to lower case.
    def preProcessLyrics(self, lyrics):
        stop_words = set(stopwords.words('english')) 
        #get an array of all the words
        words = re.findall(r'\w+', lyrics)
        filtered_lyrics = []
        for word in words:
            if word not in stop_words:
                filtered_lyrics.append(word)
        return filtered_lyrics

    # Pretty printing ;)
    def getProfilesForAllArtists(self):
        for artist in self.songsPerArtist:
            print(artist)
            words_and_tf_idf = self.calculcatetfIdf(self.songsPerArtist[artist])
            for word in words_and_tf_idf:
                print(word + ": " + str(words_and_tf_idf[word]))
        

#Instatiate and run
ap = artistprofiling()
ap.getProfilesForAllArtists()

