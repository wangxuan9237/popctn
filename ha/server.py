#!/bin/env python
#-*-coding:utf-8-*-
import socket
import logging
import subprocess

def chg_restart(ip):
    f = file('/etc/haproxy/haproxy.cfg','a+')
    msg = '    server srv01 %s:80 cookie srv01 check inter 5000 rise 3 fall 3 weight 1\n'%(ip)
    logging.info(msg)
    f.write(msg)
    f.close()
    cmd = 'haproxy -f /etc/haproxy/haproxy.cfg'
    logging.info(cmd)
    res = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = res.communicate()
    logging.info('res %s %s'%(stdout,stderr))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='/opt/test.log',  
                    filemode='w')  
  
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('172.17.0.2',1024))
    sock.listen(5)
    while True:
        connection,address = sock.accept()
        logging.info('get connect from %s'%(address,))
        chg_restart(address[0])
        logging.info('ip %s'%(address[0]))
        try:
            connection.settimeout(5)
            buf = connection.recv(1024)
            logging.info('msg is %s'%(buf))
            if buf == '1':
                msg = 'welcome to server'
                connection.send(msg)
                logging.info('send msg %s'%(msg))
            else:
                msg = 'please go out'
                connection.send(msg)
                logging.info('send %s'%(msg))
        except socket.timeout:
            logging.info('time out')
        connection.close()
