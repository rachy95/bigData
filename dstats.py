import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import csv, os, sys, re
import operator
from nltk.corpus import stopwords


 
#artist,song,link,text
class dstats(object):
    songs = []

    # Initializes the class, opens the file and puts the values of rows into a global list called 'songs' 
    # in which they are stored in a dictionary format.
    def __init__(self):
        sys.stdin.readline()
        for songRow in csv.reader(iter(sys.stdin.readline, '')):
            song = {"artist":  songRow[0],
            "song": songRow[1],
            "link": songRow[2],
            "lyrics": songRow[3]}
            self.songs.append(song)

    # Goes through the 'song' list and gets a list of artists.
    def getArtists(self):
        artists = []
        for songRow in self.songs:
            artist = songRow["artist"]
            if artist not in artists:
                artists.append(artist)
        return artists
    
    # Goes through the 'song' list and get a list of the lyrics.
    def getLyrics(self):
        lyrics = []
        for song in self.songs:
            lyrics.append(song["lyrics"])
            
        return lyrics


    # Retrieves the number of artists.
    def numOfArtists(self):
        return len(self.getArtists())

    # Retrieves the average number of songs per artist.
    def avgNumOfSongs(self):
        return self.numOfSongs()/self.numOfArtists()

    # Returns the total number of songs.
    def numOfSongs(self):
        return len(self.songs)
    
    def getNumberOfSongsPerArtist(self):
        artistsAndTotalNumberofSongs = {}
        for song in self.songs:
            artist = song["artist"]
            if artist in artistsAndTotalNumberofSongs:
                artistsAndTotalNumberofSongs[artist] += 1
            else:
                artistsAndTotalNumberofSongs[artist] = 1
        return artistsAndTotalNumberofSongs

    # Returns the number of unique words per song.
    def getWordCounts(self): 
        artistsAndUniqueWordsPerSong = {}
        totalNumOfWords = 0
        
        for song in self.songs:
            lyrics = song["lyrics"]
            words = self.preProcessLyrics(lyrics)
            allWordsInSong = []
            wordCount = 0
            nonUniqueCount = 0
            for word in words:
                wordCount = wordCount + 1
                if word not in allWordsInSong:
                    allWordsInSong.append(word)
                else:
                    nonUniqueCount = nonUniqueCount + 1

            #add the artist to the map if it does not exist and their unique words
            artist = song["artist"]
            uniqueWordsPerArtist = (wordCount - nonUniqueCount)
            if artist in artistsAndUniqueWordsPerSong:
                artistsAndUniqueWordsPerSong[artist] += uniqueWordsPerArtist
            else:
                artistsAndUniqueWordsPerSong[artist] = uniqueWordsPerArtist

            totalNumOfWords +=  wordCount

        return {"artistsAndUniqueWords":artistsAndUniqueWordsPerSong,
                "totalNumOfWords": totalNumOfWords}
    
    # Returns the average number of unique words per song.
    def avgNumOfWords(self):
        wordCounts = self.getWordCounts()
        
        sumOfUniqueWords = 0
        artistsAndUniqueWords = wordCounts["artistsAndUniqueWords"]
        for item in artistsAndUniqueWords:
            uniqueWordsPerArtist = artistsAndUniqueWords[item]
            sumOfUniqueWords += uniqueWordsPerArtist
        return (sumOfUniqueWords/self.numOfSongs())

    def preProcessLyrics(self, lyrics):
        stop_words = set(stopwords.words('english')) 
        #get an array of all the words
        words = re.findall(r'\w+', lyrics)
        filtered_lyrics = []
        for word in words:
            word = word.lower()
            if word not in stop_words:
                filtered_lyrics.append(word)
        return filtered_lyrics

    # Returns the average number of unique words per artist
    #we get the average number by dividing the unique words for all songs by their 
    # total number of songs
    def pairsOfArtistAvgNumOfWords(self):
        wordCounts = self.getWordCounts()
        artistsAndUniqueWords = wordCounts["artistsAndUniqueWords"]
        artistsAndTotalNumOfSongs = self.getNumberOfSongsPerArtist()
        artistsWithAvgUniqueWords = {}

        for artist in artistsAndUniqueWords:
            artistsWithAvgUniqueWords[artist] = artistsAndUniqueWords[artist]/artistsAndTotalNumOfSongs[artist]
        
        return artistsWithAvgUniqueWords

    def printPairsOfArtistAvgNumOfWords(self):
        print ("pairsOfArtistAvgNumOfWords: ")
        artistsAndUniqueWords = self.pairsOfArtistAvgNumOfWords()
        for key in sorted(artistsAndUniqueWords.keys()):
            print ('%s: %f' % (key, artistsAndUniqueWords[key]))

    def plotGraphOfArtistsAgainstUniqueWords(self):
        #Question 6 - plot the graph
        artistsAndUniqueWords = self.pairsOfArtistAvgNumOfWords()
        topArtists = dict(sorted(artistsAndUniqueWords.items(), key=operator.itemgetter(1), reverse=True)[:10])

        artists = []
        avgNumOfWords = []
        for key in sorted(topArtists.keys()):
            artists.append(key)
            avgNumOfWords.append(topArtists[key])


        y_pos = np.arange(len(artists))

        plt.bar(y_pos, avgNumOfWords, align='center', alpha=0.5)
        plt.xticks(y_pos, artists)
        plt.ylabel('Average number of unique words')
        plt.title('Artist')
        
        #plt.show()
        plt.savefig('plot.png')

    
    def printResult(self):
        print ("numOfArtists: " + str(self.numOfArtists()))
        print ("numOfSongs: " + str(self.numOfSongs()))
        print ("avgNumOfSongs: " + str(self.avgNumOfSongs()))
        print ("avgNumOfWords: " + str(self.avgNumOfWords()))
        self.printPairsOfArtistAvgNumOfWords()
        self.plotGraphOfArtistsAgainstUniqueWords()


        
dstat = dstats()
dstat.printResult()


