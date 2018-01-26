# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2018 PPMessage.
# Guijin Ding, dingguijin@gmail.com
#
#

import os
import glob
import magic
import shutil
import chardet
import hashlib
import datetime
import subprocess

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import jieba
import gensim

import hanziconv

def _cur_dir():
    return os.path.dirname(__file__)

_result_dir = os.path.join(_cur_dir(), "../result")
_wiki_dir = os.path.join(_cur_dir(), "../../wiki/xml")

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()
 

def _vector():
    sentences = MySentences(_result_dir + "/token") # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences,
                                   size=200,
                                   window=10,
                                   min_count=10)
    model.save(_result_dir + "/model-word2vec/word2vec.model")
    return


def _wiki_vector():
    _wiki = gensim.corpora.WikiCorpus(_wiki_dir + "/zhwiki-latest-pages-articles.xml.bz2")
    if not _wiki:
        return

    _sentences = []
    _docs = _wiki.get_texts()
    for _doc in _docs:
        _doc = hanziconv.HanziConv.toSimplified(_doc)
        _doc = jieba.cut(_doc)
        _sentences.append(list(_doc))
    
    _model = gensim.models.Word2Vec(_sentences,
                                   size=200,
                                   window=5,
                                   min_count=5)
    
    _model.save(_result_dir + "/model-word2vec/word2vec.model")
    return


               
def _main():
    #_vector()
    _wiki_vector()
    return

if __name__ == "__main__":
    _main()
