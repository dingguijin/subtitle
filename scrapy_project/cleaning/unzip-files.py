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
import subprocess


def _cur_dir():
    return os.path.dirname(__file__)

_result_dir = os.path.join(_cur_dir(), "../result")

def _files():
    _pattern = _result_dir + "/raw/*"
    return glob.glob(_pattern)


def _copy(_f):
    _unzip = _result_dir + "/unzip/"
    _dst = _unzip + os.path.basename(_f)
    shutil.copyfile(_f, _dst)
    return

def _text(_f):
    _copy(_f)
    return

def _unrar(_f):
    _unzip = _result_dir + "/unzip/"
    _dst = _unzip + os.path.basename(_f)
    subprocess.call(["mkdir", _dst])
    subprocess.call(["unrar", "x", "-y", "-inul", _f, _dst])
    return

def _unzip(_f):
    _unzip = _result_dir + "/unzip/"
    _dst = _unzip + os.path.basename(_f)
    subprocess.call(["mkdir", _dst])
    subprocess.call(["unzip", "-o", "-qO", "UTF-8", _f, "-d", _dst])
    return

def _7z(_f):
    _unzip = _result_dir + "/unzip/"
    _dst = _unzip + os.path.basename(_f)
    subprocess.call(["mkdir", _dst])
    subprocess.call(["7z", "x", _f, "-y", "-o"+_dst])
    return



def _regs():
    _r = {
        "text/plain": _text,
        "text/python": _text,
        "application/zip": _unrar,
        "application/x-rar": _unrar,
        "application/x-7z-compressed": _7z,
        "application/octet-stream": _text
    }
    return _r

def _main():
    _s = _files()

    _handlers = _regs()
    
    #m = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
    # m = magic.Magic(flags=magic.MAGIC_NONE)
    # m.load()
    # file_type = magic.from_buffer(data)
    for _f in _s:

        if _f.split("/")[-1] == "README":
            continue


        with open(_f, "rb") as _rf:
            _data = _rf.read()
            _type = magic.from_buffer(_data[:4096], mime=True)            
            print("file:%s type: %s" % (_f, _type))
            
            _handler = _handlers.get(_type)
            if not _handler:
                print("can not handle: %s:%s" % (_type, _f))
                continue

            _handler(_f)
    
    return


if __name__ == "__main__":
    _main()
