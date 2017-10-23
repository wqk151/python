#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:ftpServer.py
@time:2016/9/27 15:07
"""
import SocketServer
import account
import os
class MyTCPHandler(SocketServer.BaseRequestHandler):
    exit_flag = False #静态字段，属于类
    def handle(self):
        while not self.exit_flag:
            #print self  #self就是类实例化的对象本身
            #print self.exit_flag
            msg = self.request.recv(1024)
            if not msg:
                break
            msg_parse = msg.split("|")
            msg_type = msg_parse[0]
            if hasattr(self,msg_type):  # 判断self 是否含所有msg_type的方法
                func = getattr(self,msg_type)   # 获取self的msg_type方法
                func(msg_parse) # 执行msg_type方法
            else:
                print '--\033[31;1mWrong msg to method %s ---' % msg_type
    def ftp_authentication(self,msg):
        auth_res = False
        if len(msg) == 3:
            msg_type,username,passwd = msg
            if account.accounts.has_key(username):
                if account.accounts[username]['passwd'] == passwd:
                    auth_res = True
                    #定义三个实例属性,动态字段
                    self.login_user = username
                    self.cur_path = '%s/%s' % (os.path.dirname(__file__),account.accounts[username]['home'])
                    self.home_path = '%s/%s' % (os.path.dirname(__file__),account.accounts[username]['home'])
                else:
                    auth_res = False
            else:
                auth_res = False
        else:
            auth_res = False
        if auth_res:
            msg = "%s :: success" % msg_type
            print '\033[032;1muser:%s has passed authentication!\033[0m' % username
        else:
            msg = "%s :: failed" % msg_type
    def has_privilege(self,path):
        abs_path = os.path.abspath(path)    # 返回绝对路径
        if abs_path.startswith(self.home_path):  # 判断路径是否以指定字符串开头
            return True
        else:
            return False
    def file_transfer(self,msg):
        transfer_type = msg[1]
        filename = '%s/%s' % (self.cur_path,msg[2])
        self.has_privilege(filename)
        if transfer_type == 'get':
            if os.path.isfile(filename) and self.has_privilege(filename):
                file_size = os.path.getsize(filename)
                confirm_msg = "file_transfer::get__file::send_ready::%s" % file_size
                self.request.send(confirm_msg)
                client_confirm_msg = self.request.recv(1024)
                if client_confirm_msg == "file_transfer::get_file::recv_ready":
                    f = file(filename,'rb')
                    size_left =file_size
                    while size_left >0:
                        if size_left<1024:
                            self.request.send(f.read(size_left))
                        else:
                            self.request.send(f.read(1024))
                            size_left -=1024
                    else:
                        print "send file done ..."
            else:
                err_msg = "file_transfer::get_file::error::file does not exit or is a directory"
                self.request.send(err_msg)
        elif transfer_type =='put':
            filename,file_size = msg[-2],int(msg[-1])
            filename ="%s/%s" % (self.cur_path,filename)
            print "filename:",filename
            if os.path.isfile(filename):
                f = file('%s.0'%(filename),'wb')
            else:
                f = file('%s' %(filename),'wb')
            confirm_msg = "file_transfer::put_file::recv_ready"
            self.request.send(confirm_msg)
            recv_size =0
            while not recv_size == file_size:
                data = self.request.recv(1024)
                recv_size += len(data)
                f.write(data)
            else:
                print "--\033[32;1mReceiving file:%s done\033[0m--" % filename
                f.close()







