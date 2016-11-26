FROM centos7:v0.9
RUN yum install -y httpd net-tools vim
COPY httpd.conf /etc/httpd/conf/
COPY start.sh /opt/
COPY client.py /opt/
CMD httpd -k start;sh /opt/start.sh;while true;do sleep 10;done
