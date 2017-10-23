#!/bin/bash
#__author__ = "Administrator"
#__date__="2016/9/9"
#__time__="16:51"
source common.sh
cd  ${SOFTWARE_DIR}nrpe
./configure --prefix=${APP_DIR}nagios
make all
make install-plugin
make install-daemon
make install-daemon-config

#\mv /opt/tool/nagios/tool/nrpe.cfg /usr/local/nagios/etc/
sed -i '/allowed_hosts/s/=.*/='${NAGIOS_HOSTNAME}'/' ${APP_DIR}nagios/etc/nrpe.cfg
echo "${APP_DIR}nagios/bin/nrpe -c ${APP_DIR}nagios/etc/nrpe.cfg -d" >> /etc/rc.local
#\mv /opt/tool/nagios/tool/check* /usr/local/nagios/libexec/
chmod a+x ${APP_DIR}nagios/libexec/*
chown -R nagios.nagios ${APP_DIR}nagios
${APP_DIR}nagios/bin/nrpe -c ${APP_DIR}nagios/etc/nrpe.cfg -d