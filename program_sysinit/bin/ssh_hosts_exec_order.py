#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:ssh_hosts_exec_order.py
@time:2016/11/8 0008 11:08
"""
import paramiko

def ssh_transport_file(host,port,user,passwd,file): # file 一个list
    #print host,port,user,passwd,file
    ssh = paramiko.Transport((host,int(port)))
    ssh.connect(username=user,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(ssh)
    for f in file:
        sftp.put(f,f)
        print "put file %s"  % f
    sftp.close()
    ssh.close()

def ssh_cmd(host,port,user,passwd,file):
    #msg = "-------result%s--------" % host
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(host,port,user,passwd)
        for f in file:
            cmd = 'sh' + ' ' +f

            stdin,stdout,stderr = s.exec_command(cmd)
            cmd_result = stdout.read(),stderr.read()
            #print msg
            print cmd
        for line in cmd_result:
            print line,
        s.close()
    except paramiko.AuthenticationException:
        #print msg
        print "AuthenticationException Failed"
    except paramiko.BadHostKeyException:
        #print msg
        print "Bad host key"

