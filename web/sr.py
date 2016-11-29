#!/usr/bin/env python
import time
import sys
import json
import random
import logging
from kazoo.client import KazooClient
from kazoo.exceptions import *
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test.log',
                    filemode='w')

class ServiceRegister:
    """
    hosts:  the connection string for zk server, such as
            '10.0.1.1:2181,10.0.1.2:2181'

    The object should be created after service has been started successfully.
    """

    def __init__(self, hosts):
        idx = hosts.find(':/')
        logging.info('The idx is %d'%(idx))
        if idx != -1:
            chroot = hosts[idx+1:]
        else:
            chroot = None
        self._hosts = hosts
        self._zk = KazooClient(self._hosts,0.1)
        self._zk.start()
        if chroot and not self._zk.exists('/'):
            self._zk.stop()
            self._zk.close()
            raise NoNodeError("%s does NOT exist in zookeeper" % chroot)
        pass

    def create_zone(self, zone):
        """
        create zone in cluster

        If the zone is already exist, do nothing, else create
        the given zone path.
        """
        try:
            self._zk.create(zone, 'zone of %s' % zone, makepath=True)
        except NodeExistsError:
            pass
        except Exception as e:
            raise e
        pass

    def register(self, info):
        """
        create an ephemeral and sequence node in root with service info

        :param info: str register info that will write into znode

        """
        try:
            p = self._zk.create('/'+info, value=info, ephemeral=True, sequence=False)
        except (NoNodeError, NoChildrenForEphemeralsError, ZookeeperError) as e:
            raise e
        logging.debug('register on  %s'% p)
        #print 'register on ', p
        pass

    def get_service(self, k=0):
        """
        Select at most k service in server
        If k is None or zero, select all.
        If k is larger than all available services, return all.
        """
        svs = []
        try:
            children = self._zk.get_children('/')
        except NoNodeError as e:
            raise e
            pass
        except ZookeeperError as e:
            raise e
            pass

        if not k or k > len(children):
            k = len(children)

        choice = random.sample(children, k)
        for c in choice:
            try:
                data, stat = self._zk.get('/' + c)
                svs.append(data)
            except (NoNodeError, ZookeeperError) as e:
                logging.debug('ZookeeperError%'%e)
                #print e
                continue

        return svs
        pass

