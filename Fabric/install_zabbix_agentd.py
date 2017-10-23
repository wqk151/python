#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:fab_zabbix_agent.py
@time:2016/12/15 0015 18:24
"""
from fabric.colors import *
from fabric.api import *

env.user = 'root'
'''
env.roledefs = {
    'dbservers':[],
}
'''
env.hosts = []

env.password = '123'

#@roles('dbservers')
@task
def install_zabbix_agent():
    print yellow("Install zabbix agent...")
  #  with hide("running","stdout"):
    with settings(warn_only=True):
        run('rpm -ivh http://repo.zabbix.com/zabbix/3.2/rhel/6/x86_64/zabbix-agent-3.2.1-1.el6.x86_64.rpm')
        put("/data/sh/zabbix_agentd.conf","/etc/zabbix/zabbix_agentd.conf")
        local_hostname = run("cat /etc/sysconfig/network| grep HOSTNAME|awk -F= '{print $2}'")
        run("sed -i 's/Hostname=sftp1/Hostname=%s/' /etc/zabbix/zabbix_agentd.conf" % local_hostname)
        run("/etc/init.d/zabbix-agent start")
        run("chkconfig zabbix-agent on")


