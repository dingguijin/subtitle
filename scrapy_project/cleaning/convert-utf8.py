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


def _ascii(_f, _data):
    _data = _data.decode("utf_8", "ignore")
    _write(_data, _f)
    return

def _big5(_f, _data):
    _data = _data.decode("big5hkscs", 'ignore')
    _write(_data, _f)
    return


def _gb2312(_f, _data):
    _data = _data.decode("gb18030", 'ignore')
    _write(_data, _f)
    return

def _iso_8859_2(_f, _data):
    _data = _data.decode("iso8859_2", "ignore")
    _write(_data, _f)
    return

def _iso_8859_8(_f, _data):
    _data = _data.decode("iso8859_8", 'ignore')
    _write(_data, _f)
    return


def _utf_8(_f, _data):
    _data = _data.decode("utf_8", "ignore")
    _write(_data, _f)
    return

def _utf_8_sig(_f, _data):
    _data = _data.decode("utf_8_sig", "ignore")
    _write(_data, _f)
    return

def _utf_16le(_f, _data):
    _data = _data.decode("utf_16_le", "ignore")
    _write(_data, _f)
    return

def _utf_16be(_f, _data):
    _data = _data.decode("utf_16_be", "ignore")
    _write(_data, _f)
    return

def _windows_1251(_f, _data):
    _data = _data.decode("cp1251", 'ignore')
    _write(_data, _f)
    return

def _windows_1253(_f, _data):
    _data = _data.decode("cp1253", 'ignore')
    _write(_data, _f)
    return

def _windows_1255(_f, _data):
    _data = _data.decode("cp1255", 'ignore')
    _write(_data, _f)
    return


def _cp866(_f, _data):
    _data = _data.decode("cp866", "ignore")
    _write(_data, _f)
    return

def _cp855(_f, _data):
    _data = _data.decode("cp855", "ignore")
    _write(_data, _f)
    return


def _cp949(_f, _data):
    _data = _data.decode("cp949", 'ignore')
    _write(_data, _f)
    return


def _euc_jp(_f, _data):
    _data = _data.decode("euc_jisx0213", "ignore")
    _write(_data, _f)
    return


def _shift_jis(_f, _data):
    _data = _data.decode("shift_jis", "ignore")
    _write(_data, _f)
    return


def _not_encoded(_f, _data):
    _data = _data.decode("utf_8", "ignore")
    _write(_data, _f)
    return


def _regs():
    _r = {
        "ASCII": _ascii,
        "BIG5": _big5,

        "CP949": _cp949,

        "EUC-JP": _euc_jp,
        "GB2312": _gb2312,
        "IBM866": _cp866,
        "IBM855": _cp855,
        "ISO-8859-1": _iso_8859_2,
        "ISO-8859-2": _iso_8859_2,
        "ISO-8859-7": _iso_8859_2,
        "ISO-8859-8": _iso_8859_8,

        "SHIFT_JIS": _shift_jis,
        
        "TIS-620": _iso_8859_2,
        "UTF-8": _utf_8,
        "UTF-8-SIG": _utf_8_sig,
        "UTF-16LE": _utf_16le,
        "UTF-16BE": _utf_16be,
        "WINDOWS-1251": _windows_1251,
        "WINDOWS-1252": _windows_1251,
        "WINDOWS-1253": _windows_1253,
        "WINDOWS-1255": _windows_1255
    }
    return _r


_handlers = _regs()

def _handle_encoding(_item):

    print("handle start: %s" % datetime.datetime.now())
    
    with open(_item.get("afile"), "rb") as _file:
        _data = _file.read()

        _detect_data = _data
        if len(_data) > 2048:
            _detect_data = _data[:2048]

        # truncate data so that faster than you can imagine else slower than you can imagine
        _r = chardet.detect(_detect_data)
        
        if not _r:
            print("no encoding")
            return

        print("detect %s" % _r)

        _encoding = _r.get("encoding")
        if not _encoding:
            print("really no encoding")
            return

        print(_item.get("afile"), _encoding)

        _handler = _handlers.get(_encoding.upper())
        if not _handler:
            print("can not handle: %s:%s" % (_item.get("afile"), _encoding))
            return

        _handler(_item.get("afile"), _data)

    print("handle end: %s" % datetime.datetime.now())
    return


def _files():
    _pattern = _result_dir + "/unzip"
    _files_array = []
    for root, dirs, files in os.walk(_pattern):
        for filename in files:
            afile = os.path.join(root, filename)
            tfile = _hash(afile)
            tfile = _result_dir + "/utf8/" + tfile

            _files_array.append({"afile": afile, "tfile": tfile})



    for _item in _files_array:

        if os.path.exists(_item.get("tfile")):
            global _ignore_count
            _ignore_count = _ignore_count + 1
            #print("[%d] : ignore %s" % (_ignore_count, afile))
        else:
            print("handle %s" % (afile))
            _handle_encoding(_item)
        



def _main():
    _files()
        
    return


if __name__ == "__main__":
    _main()
