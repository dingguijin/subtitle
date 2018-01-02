import re
import os
import glob

import torch
import unicodedata

import gensim

from config import MAX_LENGTH



SOS_token = 0
EOS_token = 1
PAD_token = 2



def _cur_dir():
    return os.path.dirname(__file__)

_corpus_dir = os.path.join(_cur_dir(), "../result/token")
_word2vec_dir = os.path.join(_cur_dir(), "../result/model-word2vec")


class Voc:
    def __init__(self, model):
        self.word2vec_model = model
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS", 2:"PAD"}
        self.n_words = 3  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

# Turn a Unicode string to plain ASCII, thanks to
# http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s



def readCorpusFile(corpus):

    if corpus.endswith("README"):
        return []

    with open(corpus) as f:
        content = f.readlines()

    lines = [x.strip() for x in content]
    
    it = iter(lines)

    pairs = []

    try:
        for x in it:
            pairs.append([x, next(it)])
    except:
        pass


    it = iter(lines[1:])

    
    try:
        for x in it:
            pairs.append([x, next(it)])
    except:
        pass
    
    
        #pairs = [[x, next(it)] for x in it]
    return pairs

def readVocs():
    print("Reading Pretrained Word2Vec and Corpus...")

    _file = os.path.join(_word2vec_dir, "word2vec.model")
    _model = gensim.models.Word2Vec.load(_file)
    
    # combine every two lines into pairs and normalize

    _pairs = []

    _pattern = _corpus_dir + "/*"
    _files = glob.glob(_pattern)

    for _file in _files:
        _pair = readCorpusFile(_file)
        _pairs += _pair
    
    return Voc(_model), _pairs

def filterPair(p):
    # input sequences need to preserve the last word for EOS_token
    return len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH 

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData():
    voc, pairs = readVocs()
    print("Read {!s} sentence pairs".format(len(pairs)))
    pairs = filterPairs(pairs)
    print("Trimmed to {!s} sentence pairs".format(len(pairs)))
    print("Counting words...")
    for pair in pairs:
        voc.addSentence(pair[0])
        voc.addSentence(pair[1])
    print("Counted words:", voc.n_words)
    directory = os.path.join(save_dir, 'training_data', corpus_name) 
    if not os.path.exists(directory):
        os.makedirs(directory)
    torch.save(voc, os.path.join(directory, '{!s}.tar'.format('voc')))
    torch.save(pairs, os.path.join(directory, '{!s}.tar'.format('pairs')))
    return voc, pairs

def loadPrepareData():
    try:
        print("Start loading training data ...")
        voc = torch.load(os.path.join(save_dir, 'training_data', corpus_name, 'voc.tar'))
        pairs = torch.load(os.path.join(save_dir, 'training_data', corpus_name, 'pairs.tar'))
    except FileNotFoundError:
        print("Saved data not found, start preparing trianing data ...")
        voc, pairs = prepareData()
    return voc, pairs


# def loadPrepareData(corpus):
#     corpus_name = corpus.split('/')[-1].split('.')[0]
#     try:
#         print("Start loading training data ...")
#         voc = torch.load(os.path.join(save_dir, 'training_data', corpus_name, 'voc.tar'))
#         pairs = torch.load(os.path.join(save_dir, 'training_data', corpus_name, 'pairs.tar'))
#     except FileNotFoundError:
#         print("Saved data not found, start preparing trianing data ...")
#         voc, pairs = prepareData(corpus, corpus_name)
#     return voc, pairs


if __name__ == "__main__":
    voc, pairs = readVocs()

    print("voc:", voc, "pairs:", len(pairs))
