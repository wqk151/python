#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="nagios"
__date__="2016/9/6"
__time__="11:13"
"""
import paramiko
from multiprocessing import Pool
from hosts import HOST,ftp_host
g = HOST()
g.IP=['192.168.4.129','192.168.4.130',]
f = ftp_host()

def FilePut(ip,arg):
    script_dir=g.SCRIPT_DIR+ arg+'.sh'
    t = paramiko.Transport((ip,g.PORT))
    t.connect(username=g.USERNAME,password=g.PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(script_dir,script_dir)
    t.close()
'''
t = paramiko.Transport(('192.168.4.129',22))
t.connect(username='root',password='123456')
sftp = paramiko.SFTPClient.from_transport(t)
sftp.put('/mnt/a.sh','/tmp/a.sh')   # 必须指定上传后的目录和文件名，不能是/tmp/
t.close()
'''

def ssh_exec_script(ip,arg):
    exec_script='sh  '+g.SCRIPT_DIR +arg+'.sh'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,g.PORT,g.USERNAME,g.PASSWORD)
    stdin,stdout,stderr = ssh.exec_command(exec_script)
    print stdout.read()
    ssh.close()
'''
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.4.129',22,'root','123456')
stdin,stdout,stderr = ssh.exec_command('sh /tmp/a.sh  tom') # tom 是a.sh的位置参数
print stdout.read()
ssh.close()
'''

def down_software(arg):
    f.mk_dir()
    local_dir=f.LOCAL_TOOL_DIR+arg+'.tar.gz'
    remote_dir=f.REMOTE_TOOL_DIR +arg+'/'+arg+'.tar.gz'
    t = paramiko.Transport((f.IP,f.PORT))
    t.connect(username=f.USERNAME,password=f.PASSWD)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remote_dir,local_dir)
    t.close()

p = Pool(processes=4)
def IPprocess(arg):
    down_software(arg)
    for i in range(len(g.IP)):
        ip = g.IP[i]
        p.apply_async(FilePut,[ip,arg]).get()
        p.apply_async(ssh_exec_script,[ip,arg]).get()


