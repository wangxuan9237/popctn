FROM centos7:v0.9
RUN rm -rf /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
RUN yum clean all;yum makecache
RUN yum install -y httpd net-tools python-six
ADD setuptools-29.0.1.tar.gz /opt/
RUN cd /opt/setuptools-29.0.1/;python setup.py install
ADD kazoo-master.tar.gz /opt/
RUN cd /opt/kazoo-master/;python setup.py install
COPY httpd.conf /etc/httpd/conf/
COPY start.sh /opt/
COPY client.py /opt/
COPY sr.py /opt/
COPY zk.cfg /opt/
COPY reg.py /opt/
CMD httpd -k start;sh /opt/start.sh
