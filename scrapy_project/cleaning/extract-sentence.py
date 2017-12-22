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

def _meta_filter(line):
    _metas = ["字幕来源：", "网站地址：", "字幕组", "翻译＆校对", "字幕转制", "感谢原字幕制作者"]
    for _meta in _metas:
        if line.find(_meta) >= 0:
            return None
    return line

def _write_sentence(_ds, _from):
    to_file = _result_dir + "/sentence/" + os.path.basename(_from)
    with open(to_file, "wb") as f:
        for _d in _ds:
            _d = _meta_filter(_d)
            if _d:
                _d = _d.strip()
                if _d:
                    f.write(_d+"\r\n")
    return



class Format1():
    def __init__(self, _from):
        self.from_file = _from
        return
   
    def check(self):
        _lines = []
        with open(self.from_file, "rb") as f:

            while True:
                _line = f.readline()
                if not _line:
                    return False

                _line = _line.strip()
                if _line:
                    break
                

            if _line.startswith("\xef\xbb"):
                _line = _line[3:]

            if _line == "0-1":
                return True
            
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
                    
                    if _line[0] == "<": 
                        _line = self._html_filter(_line)
                    elif _line[0] == "{":
                        _line = self._lex_filter(_line)

                    if _line:
                        _dialogues.append(_line)
                                                
                    continue
                

        if not _dialogues:
            return

        _write_sentence(_dialogues, self.from_file)
        return


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

        _write_sentence(_dialogues, self.from_file)
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
