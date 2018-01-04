# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2018 PPMessage.
# Guijin Ding, dingguijin@gmail.com
#
#

#N_TOKENS = 57

import jieba


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


def _cur_dir():
    return os.path.dirname(__file__)

_result_dir = os.path.join(_cur_dir(), "../result")

def _write_token(_ds, _from):
    to_file = _result_dir + "/token/" + os.path.basename(_from)
    with open(to_file, "wb") as f:
        for _d in _ds:
            _d = _d.strip()
            if _d:
                f.write(_d+"\r\n")
    return


def _token(_from):

    _lines = []
    with open(_from, "rb") as f:
        for line in f:
            x = jieba.cut(line, cut_all=False)
            _lines.append(" ".join(x))
    if _lines:
        _write_token(_lines, _from)
        
    return


def _files():
    _pattern = _result_dir + "/sentence/*"
    _files_array = []
    _g = glob.glob(_pattern)
    for _file in _g:
        _files_array.append(_file)

    for _file in _files_array:
        _basename = os.path.basename(_file)
        if _basename == "README":
            continue
        _token(_file)
        
               
def _main():
    _files()
    return

if __name__ == "__main__":
    _main()
