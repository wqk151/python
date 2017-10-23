#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:ftp.py
@time:2016/9/27 16:52
"""
import SocketServer,os
class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        base_path = 'G:/tmp'
        conn = self.request
        print 'connected...'
        while True:
            per_data = conn.recv(1024)
            cmd,file_name,file_size = per_data.split('|')   #获取请求方法，文件名，文件大小
            recv_size = 0   # 已接收文件的大小
            file_dir = os.path.join(base_path,file_name)    #上传文件路径拼接
            f = file(file_dir,'wb')
            Flag = True
            while Flag:
                if int(file_size) > recv_size:
                    data = conn.recv(1024)
                    recv_size+=len(data)
                else:
                    recv_size=0
                    Flag=False
                    continue
                f.write(data)
            print 'upload successed'
            f.close()
if __name__ == '__main__':
    instance = SocketServer.ThreadingTCPServer(('127.0.0.1',8888),MyServer)
    instance.serve_forever()


