#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:pshell.py
@time:2017/2/14 0014 14:13
"""
"""
执行远程shell命令的入口文件
执行远程命令示例：
python pshell.py ls
python pshell.py  cat /data/sh/a.py
python pshell.py ls /data/sh
python pshell.py  sed -n '1,10p' /data/sh/a.py
python pshell.py  awk '{print $2}' /data/sh/11
不能执行wc -l
管道符-整个命令需要加引号
"""
import sys
import commands
cmd =  ' '.join(sys.argv[1:])


def go(cmd):
    if ',' in cmd:  #处理sed命令
        cmd = cmd.replace(',','\,')
    if '$' in cmd:  # 处理AWK命令
        cmd = cmd.replace('$','\$')
    if cmd.startswith('awk'):   #处理AWK命令
        cmd = cmd.replace("{","'{")
        cmd = cmd.replace("}","}'")
    if cmd == 'list':
        print """
some Common commands:
1、uat: tailf /opt/workspace/tomcat/apache-tomcat-7.0.57/logs/catalina.out
2、test: grep "史丙喜" /opt/workspace/tomcat/logs/catalina-2017-02-23.out
3、formal: /opt/workspace/tomcat/logs/catalina-2017-02-19.out

        """
        sys.exit()
    data = commands.getoutput('fab -f /data/sh/fabfile.py execCommand:"%s"' % cmd)      # cmd为awk命令时需要用双引号包括
    return data
print go(cmd)
