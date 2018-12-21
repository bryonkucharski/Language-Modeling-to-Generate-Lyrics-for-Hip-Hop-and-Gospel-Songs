import os
import random
import sys

from collections import Counter
from collections import defaultdict

from process import *
from generate import *
from math import log, exp

alpha = 0.01


def perplexity2(song_lyrics, frequencies):
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
    return exp(- s / n)


def perplexity3(song_lyrics, frequencies):
    s = 0
    n = 0
    for line in song_lyrics.splitlines():
        uncap_line = smart_uncapitalize(line)
        tokens = tokenize(uncap_line) # Avoid distinguishing first word of line
        len_tokens = len(tokens)

        if len_tokens > 0:
            for i in range(len_tokens):
                n += 1
                if i == 0:
                    if tokens[i] in frequencies[TRIGRAMS][(START_LINE_TOKEN, START_LINE_TOKEN)]:
                        s += log(frequencies[TRIGRAMS][(START_LINE_TOKEN, START_LINE_TOKEN)][tokens[i]])
                    elif tokens[i] in frequencies[BIGRAMS][START_LINE_TOKEN]:
                        s += log(frequencies[BIGRAMS][START_LINE_TOKEN][tokens[i]])
                    else:
                        s += 0.01
                elif i <= len_tokens - 1:
                    if (tokens[i-2],tokens[i-1]) in frequencies[TRIGRAMS] and tokens[i] in frequencies[TRIGRAMS][(tokens[i-2],tokens[i-1])]:
                        s += log(frequencies[TRIGRAMS][(tokens[i-2],tokens[i-1])][tokens[i]])
                    elif tokens[i-1] in frequencies[BIGRAMS] and tokens[i] in frequencies[BIGRAMS][tokens[i-1]]:
                        s += log(frequencies[BIGRAMS][tokens[i-1]][tokens[i]])
                    else:
                        s += 0.01
            if (tokens[len_tokens - 2],tokens[len_tokens - 1]) in frequencies[TRIGRAMS]:
                s += log(frequencies[TRIGRAMS][(tokens[len_tokens - 2],tokens[len_tokens - 1])][END_LINE_TOKEN])
            elif tokens[len_tokens - 1] in frequencies[BIGRAMS]:
                s += log(frequencies[BIGRAMS][tokens[len_tokens - 1]][END_LINE_TOKEN])
            else:
                s += 0.01
            n += 1
    return exp(- s/n)
#


# Generate a song
if __name__ == '__main__':

    # # TODO: remove below once options are implemented

    frequencies = process.compute_frequencies(json_load())

    print("Finish loading frequencies")
    with open("10_hiphop_songs.txt", encoding="latin-1") as f:
        created_song = f.read().split('\n\n')
        print(len(created_song))
        count = 0
        for song in created_song:
            pp3 = perplexity3(song, frequencies)
            print(pp3)
            count += pp3
        print("avg:", count/10)

    pps3 = 0
    pps2 = 0
    ppn = 0
    test_lyrics_texts = [read_file(filename) for filename in
                    collect_files(['/Users/weiqiuyou/Documents/UMass/2018Fall/COMPSCI585/project/new-ngrams/version2/gospel_dataset_single_file_v2_valid.txt'], True)]
    for test_lyrics_text in test_lyrics_texts:
        pps3 += perplexity3(test_lyrics_text, frequencies)
        ppn += 1
    print("test data trigram", pps3/ppn)