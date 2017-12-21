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
            try:
                _line = int(_line)
                return True
            except:
                return False
        return False

    def sentence(self):

        _dialogues = []
        _state = "NULL"

        with open(self.from_file, "rb") as f:
            while True:
                _line = f.readline()
                if not _line:
                    break
            
                _line = _line.strip()
                if not _line:
                    _state = "NULL"
                    continue
                                    
                if _state == "NULL":
                    try:
                        _n = int(_line)
                        _state  = "NUMBER"
                        continue
                    except:
                        continue
                
                if _state == "NUMBER":
                    if _line.find("-->") == -1:
                        continue
                    else:
                        _state = "POSITION"
                        continue

                if _state == "POSITION":
                    if len(_line) > 128:
                        continue

                    _line = self._meta_filter(_line)

                    if not _line:
                        continue
                    
                    if _line[0] == "<": 
                        _line = self._html_filter(_line)
                    elif _line[0] == "{":
                        _line = self._lex_filter(_line)

                    if _line:
                        _dialogues.append(_line)
                                                
                    continue
                

        if not _dialogues:
            return

        to_file = _result_dir + "/sentence/all-in-one.txt"
        with open(to_file, "wb") as f:
            for _d in _dialogues:
                f.write(_d+"\r\n")
                            
        return


    def _meta_filter(self, line):
        _metas = ["字幕来源：", "网站地址："]
        for _meta in _metas:
            if line.find(_meta) >= 0:
                return None

        return line

    def _remove_tag(self, line, begin, end):
        _status = "NULL"

        _line = []
        for c in line:
            if _status == "NULL":
                if c == begin:
                    _status = "OPEN"
                continue

            if _status == "OPEN":
                if c == end:
                    _status = "CLOSE"
                continue
            
            if _status == "CLOSE":

                if c == begin:
                    _status = "OPEN"
                    continue
                
                _line.append(c)
                continue

        return "".join(_line)
    
    def _html_filter(self, line):
        if line.find("-----") > 0:
            return None

        if line.find("-=http") > 0:
            return None

        if line.startswith("</"):
            return None

        line = self._remove_tag(line, "<", ">")

        return line

    def _lex_filter(self, line):

        if line.startswith("{\pos"):
            return None

        _line = line.split("}")[-1]

        return _line


class Format2():
    def __init__(self, _from):
        self.from_file = _from
        return
    
    def check(self):
        with open(self.from_file, "rb") as f:
            _line = f.readline()
            _line = _line.strip()            
            if _line == "[Script Info]":
                return True
            
        return False

    def sentence(self):
        _dialogues = []
        with open(self.from_file, "rb") as f:
            while True:
                _line = f.readline()
                if not _line:
                    break

                if not _line.startswith("Dialogue"):
                    continue

                _ss = _line.split("}")
                if len(_ss) == 2:
                    if len(_ss[-1]) > 256:
                        continue
                    _dialogues.append(_ss[-1])

        _to_file = _result_dir + "/sentence/" + os.path.basename(self.from_file)
        with open(_to_file, "wb") as f:
            for _d in _dialogues:
                f.write(_d)
            
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
        
        #print("handle %s" % (_file))
        
def _main():
    _files()
    return

if __name__ == "__main__":
    _main()
