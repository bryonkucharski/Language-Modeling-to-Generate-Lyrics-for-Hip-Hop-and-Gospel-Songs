###############################################################################
# Language Modeling on Penn Tree Bank
#
# This file generates new sentences sampled from the language model
#
###############################################################################

import argparse

import torch
from torch.autograd import Variable

import data
import models
import pickle

parser = argparse.ArgumentParser(description='PyTorch PTB Language Model')

# Model parameters.
parser.add_argument('--data', type=str, default='/input',
                    help='location of the data corpus')
parser.add_argument('--checkpoint', type=str, default='/model/model.pt',
                    help='model checkpoint to use')
parser.add_argument('--outf', type=str, default='/output/generated.txt',
                    help='output file for generated text')
parser.add_argument('--words', type=int, default='1000',
                    help='number of words to generate')
parser.add_argument('--temperature', type=float, default=1.0,
                    help='temperature - higher will increase diversity')
parser.add_argument('--model', type=str, default='LSTM',
                    help='type of recurrent net (RNN_TANH, RNN_RELU, LSTM, GRU)')
parser.add_argument('--emsize', type=int, default=200,
                    help='size of word embeddings')
parser.add_argument('--nhid', type=int, default=200,
                    help='number of hidden units per layer')
parser.add_argument('--nlayers', type=int, default=2,
                    help='number of layers')
parser.add_argument('--lr', type=float, default=20,
                    help='initial learning rate')
parser.add_argument('--clip', type=float, default=0.25,
                    help='gradient clipping')
parser.add_argument('--epochs', type=int, default=40,
                    help='upper epoch limit')
parser.add_argument('--batch_size', type=int, default=20, metavar='N',
                    help='batch size')
parser.add_argument('--bptt', type=int, default=35,
                    help='sequence length')
parser.add_argument('--dropout', type=float, default=0.2,
                    help='dropout applied to layers (0 = no dropout)')
parser.add_argument('--tied', action='store_true',
                    help='tie the word embedding and softmax weights')
parser.add_argument('--seed', type=int, default=1111,
                    help='random seed')
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--log-interval', type=int, default=200, metavar='N',
                    help='report interval')
parser.add_argument('--save', type=str,  default='/output/model.pt', # /output
                    help='path to save the final model')
parser.add_argument('--output_file', type=str,  default='hiphop_output.txt', # /output
                    help='path to save the final model')
args = parser.parse_args()

# Set the random seed manually for reproducibility.
#torch.manual_seed(args.seed)
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")
    #else:
        #torch.cuda.manual_seed(args.seed)

if args.temperature < 1e-3:
    parser.error("--temperature has to be greater or equal 1e-3")


if args.output_file == 'gospel_output.txt':
    '''
    corpus = data.Corpus(train_path='../../data/version2/gospel_dataset_single_file_v2_train.txt',
                         test_path='../../data/version2/gospel_dataset_single_file_v2_test.txt',
                         valid_path='../../data/version2/gospel_dataset_single_file_v2_valid.txt')
    ntokens = len(corpus.dictionary)
    filehandler = open('gospel_corpus.txt', 'wb')
    pickle.dump(corpus, filehandler)
    '''
    filehandler = open('gospel_corpus.txt', 'rb')
    corpus = pickle.load(filehandler)
    print('corpus loaded')
    ntokens = len(corpus.dictionary)


    model = models.RNNModel(args.model, ntokens, args.emsize, args.nhid, args.nlayers, args.dropout, args.tied)
    model.load_state_dict(torch.load('gospel_lm_v2.pt'))

elif args.output_file == 'hiphop_output.txt':
    '''
    corpus = data.Corpus(train_path='../../data/version2/hip_hop_dataset_single_file_v2_train.txt',
                         test_path='../../data/version2/hip_hop_dataset_single_file_v2_test.txt',
                         valid_path='../../data/version2/hip_hop_dataset_single_file_v2_valid.txt')
    ntokens = len(corpus.dictionary)
    '''
    filehandler = open('hip_hop_corpus.txt', 'rb')
    corpus = pickle.load(filehandler)
    print('corpus loaded')
    ntokens = len(corpus.dictionary)
    model = models.RNNModel(args.model, ntokens, args.emsize, args.nhid, args.nlayers, args.dropout, args.tied)
    model.load_state_dict(torch.load('hiphop_lm_v2.pt'))




model.eval()

if args.cuda:
    model.cuda()
else:
    model.cpu()

print(corpus.test)
with open(args.output_file, 'w') as outf:


    hidden = model.init_hidden(1)
    #start_words = ['god', 'drugs', 'sex']
    start_word = 'drugs'
    input = Variable(torch.tensor([[corpus.dictionary.word2idx[start_word]]]), volatile=True)
    #input = Variable(torch.rand(1, 1).mul(ntokens).long(), volatile=True)
    start_word = corpus.dictionary.idx2word[input]
    outf.write(start_word + " ")
    print(start_word + " ", end = '')
    if args.cuda:
        input.data = input.data.cuda()

    while True:
        output, hidden = model(input, hidden)
        word_weights = output.squeeze().data.div(args.temperature).exp().cpu()

        word_idx = torch.multinomial(word_weights, 1)[0]
        input.data.fill_(word_idx)
        word = corpus.dictionary.idx2word[word_idx]
        if word == "<eol>":
            break
        elif word ==  "<eos>":
            word = '\n'
        print(word + " ", end = '')
        #word = '\n' if word == "<eos>" else word

        outf.write(word + " ")
    outf.write('=' * 89 + '\n')


