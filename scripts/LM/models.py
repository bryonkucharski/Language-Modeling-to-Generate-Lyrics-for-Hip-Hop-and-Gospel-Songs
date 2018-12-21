import torch.nn as nn
from torch.autograd import Variable




def repackage_hidden(h):
  """Wraps hidden states in new Variables, to detach them from their history."""
  if type(h) == Variable:
    return Variable(h.data)
  else:
    return tuple(repackage_hidden(v) for v in h)

    
class LM_LSTM(nn.Module):
  """Simple LSMT-based language model"""
  def __init__(self, embedding_dim, num_steps, batch_size, vocab_size, num_layers, dp_keep_prob):
    super(LM_LSTM, self).__init__()
    self.embedding_dim = embedding_dim
    self.num_steps = num_steps
    self.batch_size = batch_size
    self.vocab_size = vocab_size
    self.dp_keep_prob = dp_keep_prob
    self.num_layers = num_layers
    self.dropout = nn.Dropout(1 - dp_keep_prob)
    self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
    self.lstm = nn.LSTM(input_size=embedding_dim,
                            hidden_size=embedding_dim,
                            num_layers=num_layers,
                            dropout=1 - dp_keep_prob)
    self.sm_fc = nn.Linear(in_features=embedding_dim,
                           out_features=vocab_size)
    self.init_weights()

  def init_weights(self):
    init_range = 0.1
    self.word_embeddings.weight.data.uniform_(-init_range, init_range)
    self.sm_fc.bias.data.fill_(0.0)
    self.sm_fc.weight.data.uniform_(-init_range, init_range)

  def init_hidden(self):
    weight = next(self.parameters()).data
    return (Variable(weight.new(self.num_layers, self.batch_size, self.embedding_dim).zero_()),
            Variable(weight.new(self.num_layers, self.batch_size, self.embedding_dim).zero_()))

  def forward(self, inputs, hidden):
    embeds = self.dropout(self.word_embeddings(inputs))
    lstm_out, hidden = self.lstm(embeds, hidden)
    lstm_out = self.dropout(lstm_out)
    logits = self.sm_fc(lstm_out.view(-1, self.embedding_dim))
    return logits.view(self.num_steps, self.batch_size, self.vocab_size), hidden


class RNNModel(nn.Module):
    def __init__(self, rnn_type, ntoken, ninp, nhid, nlayers, dropout=0.5, tie_weights=False):
        super(RNNModel, self).__init__()
        self.drop = nn.Dropout(dropout)
        self.encoder = nn.Embedding(ntoken, ninp) # Token2Embeddings
        if rnn_type in ['LSTM', 'GRU']:
            self.rnn = getattr(nn, rnn_type)(ninp, nhid, nlayers, dropout=dropout)
        else:
            try:
                nonlinearity = {'RNN_TANH': 'tanh', 'RNN_RELU': 'relu'}[rnn_type]
            except KeyError:
                raise ValueError( """An invalid option for `--model` was supplied,
                                options are ['LSTM', 'GRU', 'RNN_TANH' or 'RNN_RELU']""")
            self.rnn = nn.RNN(ninp, nhid, nlayers, nonlinearity=nonlinearity, dropout=dropout)
        self.decoder = nn.Linear(nhid, ntoken)

          # Optionally tie weights as in:
          # "Using the Output Embedding to Improve Language Models" (Press & Wolf 2016)
          # https://arxiv.org/abs/1608.05859
          # and
          # "Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling" (Inan et al. 2016)
          # https://arxiv.org/abs/1611.01462
        if tie_weights:
          if nhid != ninp:
              raise ValueError('When using the tied flag, nhid must be equal to emsize')
        self.decoder.weight = self.encoder.weight

        self.init_weights()

        self.rnn_type = rnn_type
        self.nhid = nhid
        self.nlayers = nlayers

    def init_weights(self):
        initrange = 0.1
        self.encoder.weight.data.uniform_(-initrange, initrange)
        self.decoder.bias.data.fill_(0)
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, input, hidden):
        emb = self.drop(self.encoder(input))
        output, hidden = self.rnn(emb, hidden)
        output = self.drop(output)
        decoded = self.decoder(output.view(output.size(0)*output.size(1), output.size(2)))
        return decoded.view(output.size(0), output.size(1), decoded.size(1)), hidden

    def init_hidden(self, bsz):
        weight = next(self.parameters()).data
        if self.rnn_type == 'LSTM':
          return (Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()),
                  Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()))
        else:
          return Variable(weight.new(self.nlayers, bsz, self.nhid).zero_())