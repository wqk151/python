#!/bin/bash
#__author__ = "Administrator"
#__date__="2016/9/12"
#__time__="17:00"
source common.sh
yum -y install  gcc gcc-c++ gcc-g77 autoconf automake zlib* fiex* libxml* ncurses-devel libtool-ltdl-devel* make cmake library  bison-devel
#make user and group
groupadd mysql
useradd -s /sbin/nologin -g mysql -M mysql

#mkdir
MYSQL_INSTALL_DIR=${APP_DIR}mysql
MYSQL_DATA_DIR=${WORKSPACE_DIR}mysql
mkdir -p $MYSQL_INSTALL_DIR
mkdir -p $MYSQL_DATA_DIR
mkdir -p $MYSQL_INSTALL_DIR/logs



cd ${SOFTWARE_DIR}mysql  && cmake \
-DMYSQL_USER=mysql \
-DCMAKE_INSTALL_PREFIX=/data/apps/mysql \
-DMYSQL_DATADIR=/data/workspace/mysql \
-DMYSQL_UNIX_ADDR=/data/apps/mysql.sock \
-DSYSCONFDIR=/data/apps/mysql/ \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_MEMORY_STORAGE_ENGINE=1 \
-DWITH_READLINE=1 \
-DMYSQL_TCP_PORT=3306 \
-DENABLED_LOCAL_INFILE=1 \
-DWITH_PARTITION_STORAGE_ENGINE=1 \
-DEXTRA_CHARSETS=all \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DWITH_READLINE=1


make && make install

mv /etc/my.cnf /tmp/my.cnf-bak

#Initialize database
${MYSQL_INSTALL_DIR}/scripts/mysql_install_db  --datadir=${MYSQL_DATA_DIR} --user=mysql --basedir=${MYSQL_INSTALL_DIR}

chown -R mysql:mysql /data/apps/mysql/
# add service and start mysql with system on
cp ${MYSQL_INSTALL_DIR}/support-files/mysql.server /etc/init.d/mysql
cp ${MYSQL_INSTALL_DIR}/bin/mysql /bin/
sed -i "/\[mysqld\]/a\datadir="${MYSQL_DATA_DIR}"" ${MYSQL_INSTALL_DIR}/my.cnf
sed -i "/\[mysqld\]/a\log_error="${MYSQL_INSTALL_DIR}"/logs/error.log" ${MYSQL_INSTALL_DIR}/my.cnf
# sed -i "/\[mysqld\]/a\socket = "${SOFTWARE_DIR}${S_NAME}"/mysql.sock"   ${MYSQL_INSTALL_DIR}/my.cnf
chkconfig mysql on
/etc/init.d/mysql start


#configure environment variable
cp /etc/profile /etc/profile_$LOCAL_DATE
PATH_NUM=$(sed -n '/^PATH=\$/p' /etc/profile  |wc -l)
if [ $PATH_NUM == 0 ];then
    echo "MYSQL_HOME=${MYSQL_INSTALL_DIR}"  >> /etc/profile
    echo 'PATH=$PATH:$MYSQL_HOME/bin'  >>/etc/profile
    else
    sed -i '/^PATH=/i\MYSQL_HOME='${MYSQL_INSTALL_DIR}'' /etc/profile
    sed -i '/^PATH\=\$/s#$#:$MYSQL_HOME/bin#'  /etc/profile

fi
source /etc/profile

