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


def _cur_dir():
    return os.path.dirname(__file__)

_result_dir = os.path.join(_cur_dir(), "../result")


class Format1():
    def __init__(self, _from):
        self.from_file = _from
        return
    
    def check(self):
        _lines = []
        with open(self.from_file, "rb") as f:
            _line = f.readline()
            _line = _line.strip()
            if _line in ["0", "1", "2"]:
                return True
            
        return False

    def sentence(self):
        return



class Format2():
    def __init__(self, _from):
        self.from_file = _from
        return
    
    def check(self):
        _lines = []
        with open(self.from_file, "rb") as f:
            _line = f.readline()
            _line = _line.strip()            
            if _line == "[Script Info]":
                return True
            
        return False

    def sentence(self):
        return

def _sentence(_from):

    _obj = Format1(_from)
    if _obj.check():
        _obj.sentence()
        return

    _obj = Format2(_from)
    if _obj.check():
        _obj.sentence()
        return
    
    print("unknow .... %s" % _from)
    return


def _files():
    _pattern = _result_dir + "/extracted/*"
    _files_array = []
    _g = glob.glob(_pattern)
    for _file in _g:
        _files_array.append(_file)

    for _file in _files_array:

        _basename = os.path.basename(_file)
        if _basename == "README":
            continue
        
        _sentence(_file)
        
        print("handle %s" % (_file))
        
def _main():
    _files()
    return

if __name__ == "__main__":
    _main()
