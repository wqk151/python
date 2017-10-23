#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:system_initialization.py
@time:2017/1/3 0003 9:05
"""

# 请先配置root密码，和格式化磁盘
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/usr/sbin/'
local_file = ['pwaiwang','nmon']

env.user = 'root'
#env.hosts = []
env.hosts = []
env.password = ''
#env.gateway = ''

env.colorze_errors = True

def yum_package():
    print yellow("yum some packages")
    with settings(warn_only=True):
        run("yum install -y libselinux-python net-snmp* git bzip-devel lrzsz  wget gcc gcc-c++ ftp lftp python-devel openssl-devel PyYAML  libyaml  vim zlib zlib-devel openssh-clients  ntpdate")
        run("mkdir -p /data/{apps,workspace,sh,tools}")
def time_synchronization():
    print yellow("time synchronization")
    with settings(warn_only=True):
        run("echo '15 1 * * * /usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1' >> /var/spool/cron/root")
        run("\\cp -f  /usr/share/zoneinfo/Asia/Shanghai /etc/localtime")
        run("/usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1")

def safe_conf():
    print yellow("config iptables selinux")
    with settings(warn_only=True):
        run("/etc/init.d/iptables stop")
        run("chkconfig iptables off")
        run("/usr/sbin/setenforce 0")
        run("sed -i '7s/enforcing/disabled/' /etc/sysconfig/selinux")

def put_file():
    print yellow("put file nmon pwaiwang...")
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' + local_file[i],remote_dir + local_file[i])
            run("chmod +x %s " % (remote_dir + local_file[i]))
        if result.failed and not confirm("put  file failed,Continue[Y/N]"):
            abort("Aborting file put task")

def file_handles():
    print yellow("change file handles")
    limits = run("cat /proc/sys/fs/file-max")
    run('echo -e "* hard nofile %s\n* soft nofile %s ">> /etc/security/limits.conf  '%(limits,limits))

def change_dns():
    print yellow("change dns server")
    run("sed -i '/nameserver/s/168.63.129.16/219.141.136.10/' /etc/resolv.conf")
def configure_kernel():
    print yellow("configure kernel")
    local_time = run("date +%F")
    with cd("/etc/"):
        run("mv sysctl.conf sysctl.conf_%s" % local_time)
    put("/data/tool/sysctl.conf", "/etc/")
    run("sysctl -p")

def configure_secret_key():
    print yellow("configure secret key")
    run("mkdir -p /root/.ssh")
    run("echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA05afSXaggvhwFqwQJhpWKb8B2YZHY4mqodSNlw1dUxRa65k9Po2LeZ7vRwdrDGQHllbkBbsAmsVtcQRIzic6/VhYMPyLcKCkmmXZpY1K7ILcqiW8X9BEX+GjcYoeu2k34S/oZOz3/2HsRi3VrK3gYfZThdDF9PvCTJi5E0AtFwLkrFAslsNbfKqulhxiTLVBE/JoVZJpLxJON0lTxILj/Nw/BnsRQmiBn1hNVZSthOoCQN+Ptk6a8GxKilOvw/wQQfh9QVHQXXLfh7EW0G31/Lg81MHAc7OoeujYncmlr0c+GoAZhjSxVr4Y0xNa11IjR61F0ZipW12QvUJQ23QLJQ== root@spuppet' >>/root/.ssh/authorized_keys")
    run("chmod 600 /root/.ssh/authorized_keys")

@task
def go():
    with hide('running', 'stdout'):
        yum_package()
        time_synchronization()
        safe_conf()
        put_file()
        file_handles()
        change_dns()
        configure_kernel()
        configure_secret_key()
