#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="mongodb"
__date__="2016/8/12"
__time__="14:53"
"""
import os
import sys
import argparse

mongo_home = "/usr/local/mongodb"
mongod_bin = mongo_home + "/bin/mongod "
pid_file = "/tmp/mongodb.pid"
default_config_argvs = "--rest --fork --syslog --httpinterface --pidfilepath  " + pid_file
default_dbpath = "/data/db"


def useage():
    """用法"""
    comment = """
		start: start the mongod process
		stop: stop mongod db server
	"""
    print(comment)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--cmd', default='start',
                       help='start:start mongodb server stop:stop mongodb server ')  # check power
    if os.getuid() != 0:
        print("请切换至root进行操作")
        sys.exit(0)
    args = parse.parse_args()
    operation = args.cmd
    if operation == "start":
        # start mongod
        if len(args) == 0:
            #check db path exit
            if not os.path.isdir(default_dbpath):
                os.system('mkdir -p ' + default_dbpath)
            os.system(mongod_bin + default_config_argvs)
        else:  #使用外部参数进行启动
            print("开发中...")
            pass
    elif operation == "stop":
        os.system(mongod_bin + "--shutdown")
        pass
    else:
        useage()
        sys.exit(0)