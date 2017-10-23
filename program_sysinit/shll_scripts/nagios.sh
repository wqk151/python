#!/bin/bash
#__author__ = "Administrator"
#__date__="2016/9/9"
#__time__="15:04"
source common.sh
groupadd nagios
useradd -s /sbin/nologin -g nagios -M nagios
cd  ${SOFTWARE_DIR}nagios
./configure --prefix=${APP_DIR}nagios
make && make install
chown -R nagios.nagios ${APP_DIR}nagios
