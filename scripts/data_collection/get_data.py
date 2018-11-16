'''
This script will use pylyrics3 to webscrape lyrics and save each song as a text file
'''

import os
import errno
import pylyrics3
import unicodedata
from slugify import slugify #pip install python-slugify
import string

artists = []
validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
print(validFilenameChars)

def removeDisallowedFilenameChars(filename):
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename.decode("utf-8")  if c in str(validFilenameChars))

artist_list = "../data/hiphop_artists.txt"
with open(artist_list, "r") as f:
    data = f.readlines()


    for line in data:
        artists.append(line.strip())
    print(artists)

lyrics = {}
i = 0
for artist in artists:
    print(artist)
    dictionary = pylyrics3.get_artist_lyrics(artist)
    artist = removeDisallowedFilenameChars(artist)
    if dictionary is not None:
        print("==========================")
        
        lyrics[artist] = dictionary
        j = 0
        for song in dictionary:
            song_file = removeDisallowedFilenameChars(song)
            print(song)

            filename = "../data/hiphopdata" + slugify(artist) + "/" + slugify(song_file) + ".txt"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            with open(filename, "w",encoding='utf-8') as f:
                try:
                    
                    f.write(dictionary[song])
                except UnicodeDecodeError:
                    print("line contains non-utf8 character")
                    
                
            j += 1
        i += 1
        print("Number of Artists: " + str(i))
