import process
from process import BIGRAMS, LINES_PER_VERSE, TOKENS_PER_LINE
from process import START_LINE_TOKEN, END_LINE_TOKEN
import generate
import os


class NGram():
    def __init__(self,n,train_folder=None,test_folder=None,model = None, output_model_name = None):
        self.n =  n                         #number of grams
        self.train_folder =  train_folder  #path to text file for training data
        self.test = test_folder           #path to text file for training data
        self.model = model                #path to text file contraining trained dictionary 
        self.output_model_name =output_model_name 

    def train(self):
        '''
        Takes the input text file and saves all data as a dictionary 
        Saves the dictionary to text file
        '''
        lyrics_texts = os.listdir(self.train_folder)
        print("after loading lyric files")
        lyrics_data = [process.collect_data(lyrics) for lyrics in lyrics_texts]
        print("after processing lyric files")
        aggregate_data = process.aggregate_data(lyrics_data)
        print("after aggregating lyric data")
        generate.json_save(aggregate_data, self.output_model_name)

    def test(self):
        '''
        Calculates the perplexity of the model after it has been trained
        '''
        pass
    
    def new_song(self, format,starting_sequence=None):
        '''
        Generates new outputs based on the starting_sequence
        '''
        data = generate.json_load(self.output_model_name)
        print(data)
        frequencies = process.compute_frequencies(data)
        print(generate.create_song(frequencies,  format))
    
n_gram = NGram( n = 2,
                train_folder = '../../data/hiphop_dataset_bysong/train/',
                test_folder = '../../data/hiphop_dataset_bysong/test/',
                output_model_name='hip_hop_model.txt')
#n_gram.train()
n_gram.new_song(['Verse 1', 'Chorus', 'Verse 2', 'Chorus', 'Verse 3', 'Chorus'])


