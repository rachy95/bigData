import csv, os, sys, re, nltk, math, operator
from pprint import pprint
from nltk.corpus import stopwords
  

#artist,song,link,text
class songsim(object):
    songs = []
    serialized_songs = {}
    serialized_lyrics = {}

    # Initializes the class, opens the file and puts the values of rows into a global list called 'songs' 
    # in which they are stored in a dictionary format.
    def __init__(self):
        with open("songdata.csv", "r") as songData:
            songRows = csv.reader(songData)

            next(songRows)
            i = 0
            for songRow in songRows:
                song = {
                    "title": songRow[1],
                    "lyrics": songRow[3]
                }
                self.serialized_songs[i] = songRow[1]
                self.serialized_lyrics[i] = songRow[3]
                self.songs.append(song)
                i += 1

           

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
            if word not in stop_words:
                filtered_lyrics.append(word)
        return filtered_lyrics

    def getAlltfIdf(self):
        serialized_songs_tf_idf = {}
        i = 0
        for song in self.songs:
            #we need only the keys/words as the list
            serialized_songs_tf_idf[i] = self.calculcatetfIdf(song).keys()
            i += 1

        return serialized_songs_tf_idf

    def getSong(self, songID):
        result = {}
        songTitle = self.serialized_songs[songID]
        songLyrics = self.serialized_lyrics[songID]
        for song in self.songs:
            if songTitle == song["title"] and songLyrics == song["lyrics"]:
                result = song

        return result
            

    def jaccard_similarity(self, songID, song2ID):
        #get song 1 and 2
        song1 = self.getSong(songID)
        song2 = self.getSong(song2ID)
        #calculate each song's tdidf
        song1List = self.calculcatetfIdf(song1)
        song2List = self.calculcatetfIdf(song2)
        #calculate the distance
        intersection = len(list(set(song1List).intersection(song2List)))
        union = (len(song1List) + len(song2List)) - intersection
        return float(intersection / union)


s = songsim()
# for song in sp.songs:
print(str(s.jaccard_similarity(0, 0)))
