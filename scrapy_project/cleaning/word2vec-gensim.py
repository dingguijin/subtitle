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

import gensim


def _cur_dir():
    return os.path.dirname(__file__)

_result_dir = os.path.join(_cur_dir(), "../result")


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()
 

def _vector():
    sentences = MySentences(_result_dir + "/token") # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences)
    model.save(_result_dir + "/model-word2vec/word2vec.model")
    return


               
def _main():
    _vector()
    return

if __name__ == "__main__":
    _main()
