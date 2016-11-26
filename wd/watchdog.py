#!/bin/env python
#*-*coding:utf-8-*-
import commands
import re
import logging
import time

def getUpCtn():
    p = commands.getoutput('docker ps')
    cNames = []
    tmp = p.split('\n')[1:]
    for i in tmp:
        cName = re.split('\s{2,}',i)[-1]
        cNames.append(cName)
    #['c1','c2',...]
    return cNames


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/root/docker_test/test.log',
                    filemode='w')

    while True:
        tcpu = tmem = 0.
        cNames = getUpCtn()
        logging.info('up ctn %s'%(cNames))
        for i in cNames:
            cmd = 'docker stats --no-stream %s'%i
            p = commands.getoutput(cmd)
            
            tmp = p.split('\n')[-1]
            tmp1 = re.split('\s{2,}',tmp)
            cpu = float(tmp1[1].replace('%',''))
            mem = float(tmp1[3].replace('%',''))
            logging.info('cpu %s'%(cpu))
            logging.info('mem %s'%(mem))
            tcpu += cpu
            tmem += mem
            logging.info('tcpu %s'%(tcpu))
            logging.info('tmem %s'%(tmem))
        if tcpu/len(cNames) > 10 or tmem/len(cNames)>10:
            cmd = 'docker run -d --name=web0%s web:v0.9'%(len(cNames))
            p = commands.getoutput(cmd)
            logging.ERROR('up ctn %s'%(cmd))
        time.sleep(10)

