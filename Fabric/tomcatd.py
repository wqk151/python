#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:tomcatd.py
@time:2017/1/10 0010 13:45
"""
import subprocess
import sys

order = sys.argv[1]

startTomcatScript = '/data/apps/tomcat/bin/startup.sh'
def getTomcatPid():
    psOutput = subprocess.Popen("ps aux | grep tomcat| grep -v grep|grep -v py |awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
    tomcatPid = psOutput.communicate()[0].strip()
    return tomcatPid

def stopTomcat():
    tomcatPid = getTomcatPid()
    if tomcatPid:
        subprocess.Popen("kill %s" % tomcatPid,shell=True,stdout=subprocess.PIPE).communicate()

def startTomcat():
    tomcatPid = getTomcatPid()
    if not tomcatPid:
        subprocess.Popen("%s" % startTomcatScript,shell=True,stdout=subprocess.PIPE).communicate()


if order == 'stop':
    stopTomcat()
elif order == 'start':
    startTomcat()

