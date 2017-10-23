#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:NABH.py
@time:2016/12/12 0012 17:15
"""
"""
利用paramiko的invoke_shell 机制来实现通过堡垒机实现服务器操作，原理是SSHClient.connect到堡垒机后开启一个新的SSH会话（session）运行"ssh user@ip" 去实现远程执行命令的操作。
"""
import paramiko
import os,sys,time

blip = '10.10.20.56'   #定义堡垒机信息
bluser = 'root'
blpasswd = '123456'

hostname = '10.10.20.57'   # 定义业务服务器信息
username = 'root'
password = '123456'

port = 22
passinfo = '\'s password: '     # 输入服务器密码的前标志串
paramiko.util.log_to_file('syslogin.log')   # 创建ssh连接的日志文件

ssh = paramiko.SSHClient()  # ssh登录堡垒机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=blip,username=bluser,password=blpasswd)

channel = ssh.invoke_shell()    # 创建会话，开启命令调用
channel.settimeout(30)      # 会话命令执行超时时间，单位秒

buff = ''
resp = ''
# 执行ssh登录业务主机
channel.send('ssh '+username+'@'+hostname+'\n')
time.sleep(3)
while not buff.endswith(passinfo):  # ssh登录的提示信息判断，输出串尾函数"\'s passwrod: "时，退出while循环
    try:
        resp = channel.recv(9999)
    except Exception,e:
        print 'Error info:%s connection time.' % (str(e))
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp
    if not buff.find('yes/no')==-1:     # 输出串尾含有"yes/no"时发送"yes"并回车
        channel.send('yes\n')
        buff = ''
channel.send(password + '\n')       # 发送业务主机密码

buff = ''
while not buff.endswith('# '):      # 输出串尾为"#  "时说明校验同并退出while循环
    resp = channel.recv(9999)
    if not resp.find(passinfo) == -1:   # 输出串尾含有"\'s password: "时，说明密码不正确，要求重新输入
        print 'Error info: Authentication failed.'
        channel.close()     # 关闭连接对象后退出
        ssh.close()
        sys.exit()
    buff += resp
channel.send('ifconfig\n')      # 认证通过后发送ifconfig命令查看结果
buff = ''
try:
    while buff.find('# ') == -1:
        resp = channel.recv(9999)
        buff += resp
except Exception,e:
    print 'error info:' + str(e)
print buff  # 打印输出串
channel.close()
ssh.close()


