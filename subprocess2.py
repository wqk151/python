#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:subprocess2.py
@time:2016/10/9 11:28
"""
import os
import sys
from subprocess import Popen,PIPE

list = []

cmd = 'chkconfig --list| grep "启用" | grep mongo'

for line in os.popen(cmd).readlines():
    pro = line.split(' ')[0]
    p1 = Popen(['ps','-ef'],stdout=PIPE)
    p2 = Popen(['grep','-v','grep'],stdin=p1.stdout,stdout=PIPE)
