'''
Parses the dataset taken from pylyrics3 and saves them as text files. Each song is appended to one larger text document 

'''
import numpy as np
import os
import string
import re 
from langdetect import detect_langs 


def clean_song(song, output_file, detect_foriegn = False):
    """
    Removes any special punc
    Removes foreign words
    Remove anything in paraenthesis . Rap often has "adlibs"
    Make all words lowercase
    """
    with open(song,"r",encoding='utf-8', errors='ignore') as s:
        with open(output_file, "a",encoding='utf-8', errors='ignore') as f:
            lines = s.read().splitlines()
            total_words = 0
            for line in lines:
                if line == '\n':
                    continue

                #this gets rid of anything (inside paraenthesis) or [inside brackets]
                #this is normally an 'ab-lib' which we wont count as data
                # or it is describing an artist, which we dont need
                line = re.sub("[\(\[].*?[\)\]]", "", line)
                

                #the following is taken with help from: https://machinelearningmastery.com/how-to-develop-a-word-level-neural-language-model-in-keras/
                tokens = line.split()
                # remove punctuation from each token
                table = str.maketrans('', '', string.punctuation)
                tokens = [w.translate(table) for w in tokens]
                # remove remaining tokens that are not alphabetic
                tokens = [word for word in tokens if word.isalpha()]
                # make lower case
                tokens = [word.lower() for word in tokens]


                newline = " ".join(tokens)
                if detect_foriegn:
                    try:
                        lg = detect_langs(newline)
                        for item in lg:
                            if item.lang != "en":
                            
                                print(newline + " is not detected as english", item.lang)
                                continue
                    except:
                        print("Cannot detect:" + newline)
                        continue
                total_words += len(tokens)
                f.write(newline + "\n")
    return total_words
    

output_file = "../data/hip_hop_dataset.txt"
#output_file = "../data/church_dataset.txt"

#clear file
open(output_file, "w").close()

path = '../data/hiphopdata'
#path = '../data/churchdata'

artist_folders = os.listdir(path)

number_artists = 0
number_songs = 0
number_words = 0
for artist_folder in artist_folders:
    print(number_artists)
    for song in os.listdir(path + "/" +artist_folder):
        number_words += clean_song(path + "/" +artist_folder + "/" +song, output_file)
        number_songs += 1
    number_artists += 1


print(number_artists,number_songs,number_words)

        





'''
iterate through each artist
    iterate through each song
        get all lines
        proprocess line
        append to one large .txt file
        collect stats about data (number of words, songs, artists)
'''