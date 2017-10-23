#!/bin/bash
#__author__ = "Administrator"
#__date__="2016/9/12"
#__time__="17:11"

if [ ! -f /tmp/sysinit.log ];then
    mkdir -p /data/{apps,workspace,sh,tools,update_package}
    yum -y install lrzsz libselinux-python net-snmp* git wget gcc gcc-c++  lftp python-devel openssl-devel PyYAML  libyaml  vim zlib zlib-devel openssh-clients  ntpdate
    echo "15 1 * * * /usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1" > /var/spool/cron/root
    \cp -f  /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    /usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1
    /etc/init.d/iptables stop
    chkconfig iptables off
    /usr/sbin/setenforce 0
    sed -i '7s/enforcing/disabled/' /etc/sysconfig/selinux
    echo 'HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S": '  >>/etc/profile
    mkdir -p /root/.ssh/
    cat >> /root/.ssh/authorized_keys << EOF
    ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA05afSXaggvhwFqwQJhpWKb8B2YZHY4mqodSNlw1dUxRa65k9Po2LeZ7vRwdrDGQHllbkBbsAmsVtcQRIzic6/VhYMPyLcKCkmmXZpY1K7ILcqiW8X9BEX+GjcYoeu2k34S/oZOz3/2HsRi3VrK3gYfZThdDF9PvCTJi5E0AtFwLkrFAslsNbfKqulhxiTLVBE/JoVZJpLxJON0lTxILj/Nw/BnsRQmiBn1hNVZSthOoCQN+Ptk6a8GxKilOvw/wQQfh9QVHQXXLfh7EW0G31/Lg81MHAc7OoeujYncmlr0c+GoAZhjSxVr4Y0xNa11IjR61F0ZipW12QvUJQ23QLJQ== root@spuppet
    EOF
    chmod 600 /root/.ssh/authorized_keys
    echo '50dxOp&^4V1z' | passwd --stdin root
    echo "1" >/tmp/sysinit.log
fi