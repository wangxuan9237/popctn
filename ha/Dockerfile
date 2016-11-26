FROM centos7:v0.9
RUN yum install -y haproxy net-tools vim
COPY haproxy.cfg /etc/haproxy/
COPY start.sh /opt/
COPY server.py /opt/
EXPOSE 1024
CMD sh /opt/start.sh 
