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

    
    
    """
    with open(song,"r",encoding='utf-8', errors='ignore') as s:
        with open(output_file, "a",encoding='latin-1', errors='ignore') as f:
            lines = s.read().splitlines()
            total_words = 0
            for line in lines:


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
                if len(newline) <= 1:
                    print(newline)
                    continue
                f.write(newline + "\n")
            f.write('-\n')
            
    return total_words
    
def generate_dataset(path = '../../data/hiphopdata',output_file = "../../data/hiphop_dataset_bysong/total/"):
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
    #output_file = 'hip_hop_dataset_single_file_v2.txt'
    for artist_folder in artist_folders:
        print(number_artists)
        for song in os.listdir(path + "/" +artist_folder):
            input_path = path + "/" +artist_folder + "/" +song
            #output_path = output_folder +song
            number_words += clean_song_single_file(input_path, output_file= output_file)
            number_songs += 1
        number_artists += 1


    print(number_artists,number_songs,number_words)

def test_train_split_single_file(dataset, test_percent, by = 'line'):
    '''
    dataset is a .txt file with every song
    '''
    with open(dataset, "r",encoding='utf-8', errors='ignore') as f:
        with open(dataset[:-4] + "_test.txt", "w",encoding='utf-8', errors='ignore') as a:
            with open(dataset[:-4] + "_train.txt", "w",encoding='utf-8', errors='ignore') as b:
                with open(dataset[:-4] + "_valid.txt", "w", encoding='utf-8', errors='ignore') as c:
                    if by == 'line':
                        lines = f.read().splitlines()
                    elif by == 'song':
                        lines = f.read().split('-\n')

                    length = len(lines)
                    print(length)
                    np.random.shuffle(lines)
                    num_test = int(length*test_percent)

                    train = lines[num_test:]
                    test = lines[:num_test]
                    #print(len(test))
                    #print(len(train))

                    train_length = len(train)
                    num_valid = int(train_length*.1)

                    train = train[num_valid:]
                    valid = train[:num_valid]


                    b.write('-\n'.join(str(line) for line in train))
                    a.write('-\n'.join(str(line) for line in test))
                    c.write('-\n'.join(str(line) for line in valid))


                    print(len(train))
                    print(len(valid))
                    print(len(test))

                    assert len(train) + len(valid) + len(test) == length


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


                

#generate_dataset(output_file = 'hip_hop_dataset_single_file_v2.txt') #1
#test_train_split_single_file('hip_hop_dataset_single_file_v2.txt', .2, by = 'song')
#test_train_split_folders("../../data/hiphop_dataset_bysong/total/",.2) #2


generate_dataset('../../data/gospeldata', output_file = '../../data/gospel_dataset_single_file_v2.txt')
test_train_split_single_file("../../data/gospel_dataset_single_file_v2.txt",.2,  by = 'song') #2





