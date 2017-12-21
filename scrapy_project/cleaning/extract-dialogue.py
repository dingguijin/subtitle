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


def _hash(_f):
    return hashlib.sha1(_f).hexdigest()


_ignore_count = 0
_file_count = 0


def _write(_data, _from_file):
    _data = _data.encode("utf-8")
    _to_file = _hash(_from_file)
    _to_file = _result_dir + "/utf8/" + _to_file
    with open(_to_file, "wb") as _file:
        _file.write(_data)

    global _file_count
    _file_count = _file_count + 1
    print("[%d] : %s" % (_file_count, _to_file))

    return


class Format1():
    def __init__(self, _from):
        self.from_file = _from
        return
    
    def check(self):
        _lines = []
        with open(self.from_file, "rb") as f:
            for i in range(100):
                _line = f.readline()
                if not _line:
                    break
                _lines.append(_line)
                
        if not _lines:
            return False


        _lines_0 = _lines[0].strip()
        if _lines_0 in ["0", "1", "2"]:
            return True
        
        _meets_blank = [2,3,4,5,6]

        _not_blank = 0
        for _line in _lines:

            #print("len: %d, line:%s" % (len(_line), _line))
            
            if len(_line) >= 3:
                _not_blank = _not_blank + 1
                if _not_blank > _meets_blank[-1]:
                    return False
                
            else:
                if _not_blank not in _meets_blank:
                    return False
                
                _not_blank = 0
            
        return True

    def extract(self):
        # with open(self.from_file, "rb") as f:
        #     print(f.read())

        _ed = _result_dir + "/extracted/"
        _dst = _ed + os.path.basename(self.from_file)
        subprocess.call(["mv", self.from_file, _dst])

        return


def _extract(_from):

    _obj = Format1(_from)
    if _obj.check():
        _obj.extract()
        
    return


def _files():
    _pattern = _result_dir + "/utf8/*"
    _files_array = []
    _g = glob.glob(_pattern)
    for _file in _g:
        _files_array.append(_file)

    for _file in _files_array:

        _basename = os.path.basename(_file)
        if _basename == "README":
            continue
        
        _extract(_file)
        
        print("handle %s:%s" % (_file))
        
def _main():
    _files()
        
    return


if __name__ == "__main__":
    _main()
