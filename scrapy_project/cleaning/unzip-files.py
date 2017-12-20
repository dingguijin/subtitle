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


SUBTITLE_DIR = "/opt/subtitle"

def _files():
    _pattern = SUBTITLE_DIR + "/result/*"
    return glob.glob(_pattern)


def _copy(_f):
    _unzip = SUBTITLE_DIR + "/unzip/"
    _dst = _unzip + os.path.basename(_f)
    shutil.copyfile(_f, _dst)
    return

def _text(_f):
    _copy(_f)
    return

def _unrar(_f):
    _unzip = SUBTITLE_DIR + "/unzip/"
    _dst = _unzip + os.path.basename(_f)
    subprocess.call(["mkdir", _dst])
    subprocess.call(["unrar", "x", "-y", "-inul", _f, _dst])
    return

def _unzip(_f):
    _unzip = SUBTITLE_DIR + "/unzip/"
    _dst = _unzip + os.path.basename(_f)
    subprocess.call(["mkdir", _dst])
    subprocess.call(["unzip", "-o", "-qO", "UTF-8", _f, "-d", _dst])
    return

def _7z(_f):
    _unzip = SUBTITLE_DIR + "/unzip/"
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
    
    m = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
    for _f in _s:
        _x = m.id_filename(_f)
        
        _handler = _handlers.get(_x)
        if not _handler:
            print("can not handle: %s:%s" % (_x, _f))
            continue

        _handler(_f)
        
    return


if __name__ == "__main__":
    _main()
