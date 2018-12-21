import os
import torch

class Dictionary(object):
    """Build word2idx and idx2word from Corpus(train/val/test)"""
    def __init__(self):
        self.word2idx = {} # word: index
        self.idx2word = [] # position(index): word

    def add_word(self, word):
        """Create/Update word2idx and idx2word"""
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    """Corpus Tokenizer"""
    def __init__(self, train_path, test_path, valid_path):
        self.dictionary = Dictionary()
        self.train = self.tokenize(os.path.join(train_path))
        self.valid = self.tokenize(os.path.join(valid_path))
        self.test = self.tokenize(os.path.join(test_path))

    def tokenize(self, path):
        """Tokenizes a text file."""
        assert os.path.exists(path)
        # Add words to the dictionary
        with open(path, 'r', encoding='latin-1') as f:
            tokens = 0
            for line in f:
                # line to list of token + eos
                if line == '-\n':
                    words = ['<eol>']
                else:
                    words = line.split() + ['<eos>']
                tokens += len(words)
                for word in words:
                    self.dictionary.add_word(word)

        # Tokenize file content
        with open(path, 'r', encoding='latin-1') as f:
            ids = torch.LongTensor(tokens)
            token = 0
            for line in f:
                if line == '-\n':
                     words = ['<eol>']
                else:
                    words = line.split() + ['<eos>']
                #words = line.split() + ['<eos>']
                #print(words)
                for word in words:
                    ids[token] = self.dictionary.word2idx[word]
                    token += 1

        return ids

