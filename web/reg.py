import sr
import ConfigParser
import commands
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/opt/test.log',
                    filemode='w')

    cmd = "ifconfig eth|grep -w 'inet' | awk '{print $2}'"
    logging.info('cmd:%s'%(cmd))
    IP = commands.getoutput(cmd)
    logging.info('IP:%s'%(IP))

    cfg = ConfigParser.ConfigParser()
    cfg.read('/opt/zk.cfg')
    zk_hosts = cfg.get('zookeeper','zookeeper_server')
    logging.info('zk_hosts:%s'%(zk_hosts))

    serviceReg = sr.ServiceRegister(zk_hosts)
    path = '/'+IP
    logging.info('path:%s'%(path))

    serviceReg.register(path)
    while True:
        time.sleep(10)
