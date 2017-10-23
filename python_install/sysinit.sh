#!/bin/bash
#__author__ = "Administrator"
#__date__="2016/9/12"
#__time__="17:11"

if [ ! -f /tmp/sysinit.log ];then
    mkdir -p /data/{apps,workspace,sh,tools,update_package}
    yum -y install libselinux-python net-snmp* git wget gcc gcc-c++ ftp lftp python-devel openssl-devel PyYAML  libyaml  vim zlib zlib-devel openssh-clients  ntpdate
    echo "15 1 * * * /usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1" > /var/spool/cron/root
    \cp -f  /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    /usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1
    /etc/init.d/iptables stop
    chkconfig iptables off
    /usr/sbin/setenforce 0
    sed -i '7s/enforcing/disabled/' /etc/sysconfig/selinux
    echo 'HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S": '  >>/etc/profile
    echo "1" >/tmp/sysinit.log
fi