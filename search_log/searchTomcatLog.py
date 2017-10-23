#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:searchTomcatLog.py
@time:2017/5/17 0017 18:21
"""
from fabric.colors import *
from fabric.api import *
import datetime
import ConfigParser
import os
conf = ConfigParser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conf_file = os.path.join(BASE_DIR,'conf.ini')
conf.read(conf_file)
itemlists = conf.items('webserver')
iplist = [itemlists[x][1] for x in range(len(itemlists))]
env.gateway = iplist[0]
env.hosts = iplist[1:]
# in py3 can do this
# env.gateway, *env.hosts = iplist
@task
def search_logs(argument,search_time):
    nowtime = datetime.datetime.now()
    logFormatTime = nowtime.strftime('%Y-%m-%d')
    tomcatLog = '/opt/workspace/tomcat/logs/catalina-{}.out'.format(logFormatTime)
    print green('search argument {}'.format(argument))
    with settings(warn_only=True):
        if search_time:
            run("grep --color=always -w '{}' {} | grep -v grep| grep {} || echo -e '\033[33m have no record in this server log \033[0m' ".format(argument,tomcatLog,search_time))
        else:
            run("grep --color=always -w '{}' {} | grep -v grep || echo -e '\033[33m have no record in this server log \033[0m' ".format(argument, tomcatLog,))

