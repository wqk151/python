#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:rm_win_M.py
@time:2016/11/11 0011 17:01
"""
import os
import sys
import tempfile

def main():
    filename = sys.argv[1]
    with tempfile.NamedTemporaryFile(delete=False) as fh:
        for line in open(filename):
            line = line.rstrip()
            fh.write(line + '\n')
        os.rename(filename,filename + '.bak')
        os.rename(fh.name,filename)

if __name__ == '__main__':
    main()