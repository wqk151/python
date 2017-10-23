#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:file_transport.py
@time:2016/12/13 0013 11:25
"""
"""
实现堡垒机模式下的文件上传，通过paramiko的SFTPClient将文件从办公设备上传至堡垒机指定的临时目录，如/tmp下，再通过SSHClient的invoke_shell方法开启ssh会话，执行scp命令，将/tmp下的指定文件复制到目标业务服务器上。
使用sftp.pu()方法上传至堡垒机临时 目录，再通过snd()方法执行scp命令，将堡垒机临时目录下的文件复制到目标主机。
"""
import paramiko
import os,sys,time

blip = '192.168.1.23'
bluser = 'root'
blpasswd = '123456'

hostname = '192.168.1.21'
username = 'root'
password = '123456'

tmpdir = '/tmp'
remotedir = '/data'
localpath = '/home/nginx_access.tar.gz'
tmppath = tmpdir + '/nginx_access.tar.gz'
remotepath = remotedir + '/nginx_access_hd.tar.gz'
port = 22
passinfo = '\'s password: '
paramiko.util.log_to_file('syslogin.log')

t = paramiko.Transport((blip,port))
t.connect(username=bluser,password=blpasswd)
sftp = paramiko.SFTPClient.from_transport(t)
sftp.put(localpath,tmppath)
sftp.close()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=blip,username=bluser,password=blpasswd)

channel = ssh.invoke_shell()
channel.settimeout(10)

buff = ''
resp = ''

channel.send('scp ' + tmppath + ' ' + username + '@' + hostname + ':' +remotepath + '\n')
while not buff.endswith(passinfo):
    try:
        resp = channel.recv(9999)
    except Exception,e:
        print 'Error info :%s connection time.' % str(e)
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp
    if not buff.find('yes/no') == -1:
        channel.send('yes\n')
        buff = ''
channel.send(password + '\n')
buff = ''
while not buff.endswith('# '):
    resp = channel.recv(9999)
    if not resp.find(passinfo) == -1:
        print 'Error info:Authentication failed.'
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp
print buff
channel.close()
ssh.close()