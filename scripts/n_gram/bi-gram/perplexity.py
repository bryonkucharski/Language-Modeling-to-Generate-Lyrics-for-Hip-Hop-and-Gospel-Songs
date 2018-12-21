import os
import random
import sys

from collections import Counter
from collections import defaultdict

from process import *
from generate import *
from math import log, exp

alpha = 0.01

def perplexity(song_lyrics, frequencies):
    s = 0
    n = 0
    for line in song_lyrics.splitlines():
        uncap_line = smart_uncapitalize(line)
        tokens = tokenize(uncap_line) # Avoid distinguishing first word of line
        len_tokens = len(tokens)

        if len_tokens > 0:
            for i in range(len_tokens):
                n += 1
                if i == 0: # First token: count START bigram
                    if tokens[i] in frequencies[BIGRAMS][START_LINE_TOKEN]:
                        s += log(frequencies[BIGRAMS][START_LINE_TOKEN][tokens[i]])
                    else:
                        s += 0.01
                elif i <= len_tokens - 1: # Not last token of line: count bigram
                    if tokens[i-1] in frequencies[BIGRAMS] and tokens[i] in frequencies[BIGRAMS][tokens[i-1]]:
                        s += log(frequencies[BIGRAMS][tokens[i-1]][tokens[i]])
                    else:
                        s += 0.01
            if tokens[len_tokens - 1] in frequencies[BIGRAMS]:
                s += log(frequencies[BIGRAMS][tokens[len_tokens - 1]][END_LINE_TOKEN])
            else:
                s += 0.01
            n += 1
    return exp(- s/n)

# Generate a song
if __name__ == '__main__':
    args = get_cl_args()

    # TODO: remove below once options are implemented
    if (args.preprocessed_data or
            args.n_gram_size != 2):
        print ('-n, -p, options not supported yet')
        sys.exit(1)
    if os.path.exists(MODEL_PATH):
        frequencies = process.compute_frequencies(json_load())

    else :
        lyrics_texts = [read_file(filename) for filename in
            collect_files(args.lyrics_files, args.recursive)]
        print("after loading lyric files")
        lyrics_data = [process.collect_data(lyrics) for lyrics in lyrics_texts]
        print("after processing lyric files")
        aggregate_data = process.aggregate_data(lyrics_data)
        print("after aggregating lyric data")
        json_save(aggregate_data)
        frequencies = process.compute_frequencies(aggregate_data)

    created_song = create_song(frequencies, args.song_form)
    print(created_song)
    pps = 0
    ppn = 0
    test_lyrics_texts = [read_file(filename) for filename in
                    collect_files(['/Users/weiqiuyou/Documents/UMass/2018Fall/COMPSCI585/project/data/hiphop_dataset_bysong/test'], args.recursive)]
    for test_lyrics_text in test_lyrics_texts:
        pps += perplexity(test_lyrics_text, frequencies)
        ppn += 1
    print(pps/ppn)
    pp = perplexity(created_song, frequencies)
    print(pp)
