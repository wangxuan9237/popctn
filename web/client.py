#!/bin/env python
#-*-coding:utf-8-*-

if __name__ == '__main__':
    import socket
    import time
    import logging
    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='test.log',  
                    filemode='w')  
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    logging.info('start connect')
    sock.connect(('172.17.0.2',1024))
    time.sleep(2)
    sock.send('1')
    logging.info('send 1')
    logging.info(sock.recv(1024))
    sock.close()
