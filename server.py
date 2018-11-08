# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import threading


def server(conn,addr):

    try:
        while 1:
            data = conn.recv(1024)
            file_name, file_size = str(data).split('|')
            #path = os.path.join(BASE_DIR, 'data', file_name)
            path = os.path.join('./', file_name)
            file_size = int(file_size)
            has_sent = 0
            
            with open(path, 'wb') as fp:
                while has_sent != file_size:
                    data = conn.recv(1024)
                    fp.write(data)
                    has_sent += len(data)
                    print '\r' + '[保存进度]:%s%.02f%%' % ('>' * int((has_sent / file_size) * 50), float(has_sent / file_size) * 100),
            print ' '
            print '%s 保存成功!' % file_name
    except KeyboardInterrupt:
        conn.close()
        sys.exit(-1)

if __name__ == '__main__':

    IP_PORT = ('',8888)
    s = socket.socket()
    s.bind(IP_PORT)
    s.listen(2)
    print('服务器开启成功，等待连接...')
    while True:
	    conn,addr = s.accept()
	    print '{0},{1} 已连接'. format(addr[0],addr[1])
	    t = threading.Thread(target=server,args=(conn,addr))
	    t.start()

