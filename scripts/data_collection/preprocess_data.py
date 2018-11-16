'''
Parses the dataset taken from pylyrics3 and saves them as text files. Each song is appended to one larger text document 

'''
import numpy as np
import os
import string
import re 
import shutil
import glob
import errno

def clean_song_single_file(song, output_file, detect_foriegn = False):
    """
    Takes the lyrics of one song and appends them to single text file output file

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
                if len(line) > 1:
                    
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
                    if len(tokens) > 0:
                        total_words += len(tokens)
                        f.write(newline + "\n")
            
    return total_words
    
def generate_dataset(path = '../../data/hiphopdata',output_folder = "../../data/hiphop_dataset_bysong/total/"):
    '''
    Iterate through path
    '''
   

    artist_folders = os.listdir(path)
        
    number_artists = 0
    number_songs = 0
    number_words = 0
    '''
    iterate through each artist
        iterate through each song
            get all lines
            proprocess line
            append to one large .txt file
            collect stats about data (number of words, songs, artists)
    '''
    for artist_folder in artist_folders:
        print(number_artists)
        for song in os.listdir(path + "/" +artist_folder):
            input_path = path + "/" +artist_folder + "/" +song
            output_path = output_folder +song
            open(output_path, "w+").close()
            number_words += clean_song_single_file(input_path, output_path)
            number_songs += 1
        number_artists += 1


    print(number_artists,number_songs,number_words)

def test_train_split_single_file(dataset, test_percent):
    '''
    dataset is a .txt file with every song
    '''
    with open(dataset, "r",encoding='utf-8', errors='ignore') as f:
        with open(dataset[:-4] + "_test.txt", "w",encoding='utf-8', errors='ignore') as a:
            with open(dataset[:-4] + "_train.txt", "w",encoding='utf-8', errors='ignore') as b:
                lines = f.read().splitlines()
                length = len(lines)
                print(length)
                np.random.shuffle(lines)
                num_test = int(length*test_percent)
                test = lines[num_test:]
                train = lines[:num_test]

                b.write('\n'.join(str(line) for line in train))
                a.write('\n'.join(str(line) for line in test))
                print(len(test))
                print(len(train))

def test_train_split_folders(folder, test_percent):
    '''
    folder is a path to the folder that holds all songs
    test_percent of songs will be copied to test folder, 1-test_percent of songs will be moved to train folder
    '''
    songs = os.listdir(folder)
    np.random.shuffle(songs)
    length = len(songs)
    num_test = int(length*test_percent)
    train_songs = songs[num_test:]
    test_songs = songs[:num_test]

    for song in test_songs:
        src = folder + song
        dest_folder = folder[:-6] + "/test/"
        dest = dest_folder + song

        try:
            shutil.copy(src, dest)
        except IOError as e:
            # ENOENT(2): file does not exist, raised also on missing dest parent dir
            if e.errno != errno.ENOENT:
                raise
            # try creating parent directories
            os.makedirs(os.path.dirname(dest))
            shutil.copy(src, dest)

    
    for song in train_songs:
        src = folder + song
        dest_folder = folder[:-6] + "/train/"
        dest = dest_folder + song

        try:
            shutil.copy(src, dest)
        except IOError as e:
            # ENOENT(2): file does not exist, raised also on missing dest parent dir
            if e.errno != errno.ENOENT:
                raise
            # try creating parent directories
            os.makedirs(os.path.dirname(dest))
            shutil.copy(src, dest)
                
#test_train_split('../../data/hip_hop_dataset_total.txt', .2)
#generate_dataset() #1
#test_train_split_folders("../../data/hiphop_dataset_bysong/total/",.2) #2


generate_dataset('../../data/gospeldata',"../../data/gospel_dataset_bysong/total/")
test_train_split_folders("../../data/gospel_dataset_bysong/total/",.2) #2





