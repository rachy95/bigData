import csv, os, sys, re, nltk, math, operator, argparse
from pprint import pprint
from nltk.corpus import stopwords
  

#artist,song,link,text
class artistsim(object):
    songsPerArtist = {}
    serialized_artists = {}
    artist1ID = ""
    artist2ID = ""
    # Initializes the class, opens the file and puts the values of rows into a global list called 'songs' 
    # in which they are stored in a dictionary format.
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process song similarity')
        parser.add_argument('songs_data_file', help='the name of the songs data file')
        parser.add_argument('artist1ID', help='the id of the first artist we should compare', type=int)
        parser.add_argument('artist2ID', help='the id of the second artist we should compare', type=int)


        args = parser.parse_args()
        self.artist1ID = args.artist1ID
        self.artist2ID = args.artist2ID

        with open(args.songs_data_file, "r") as songData:
            songRows = csv.reader(songData)

            next(songRows)
            #now we want a list of songs for that specific artist
            for songRow in songRows:
                artist = songRow[0]
                lyrics = songRow[3]
                if artist not in self.songsPerArtist:
                    self.songsPerArtist[artist] = lyrics
                else:
                    self.songsPerArtist[artist] += lyrics

               
            
            i = 0
            #also keep a map with all the artists names
            for artist in self.songsPerArtist:
                self.serialized_artists[i] = artist
                i += 1


    #this is for each word
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

    # this is different per song
    def calculateTermFrequency(self, lyrics):
        word_frequency = {}
        words = self.preProcessLyrics(lyrics)
        for word in words:
            if word not in word_frequency.keys():
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1
        return word_frequency

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

    # Returns artists.
    def getArtist(self, artistID):
        return self.serialized_artists[artistID]

            
    # Artists are unique because they only appear once 
    def jaccard_similarity(self, artist1, artist2):
        #calculate each artist's tdidf
        artist1List = self.calculcatetfIdf(self.songsPerArtist[artist1])
        artist2List = self.calculcatetfIdf(self.songsPerArtist[artist2])
        #calculate the distance
        intersection = len(list(set(artist1List).intersection(artist2List)))
        union = (len(artist1List) + len(artist2List)) - intersection
        return float(intersection / union)

    # Pretty printing!
    def print_result(self):
        #get the artist names
        #get artist 1 and 2
        artist1 = self.getArtist(self.artist1ID)
        artist2 = self.getArtist(self.artist2ID)
        print("The similarity between " + artist1 + " with ID " + str(self.artist1ID) + " and " + artist2 +
              " with ID " + str(self.artist2ID) + " is: ")
        print(self.jaccard_similarity(artist1, artist2))




a = artistsim()
a.print_result()

