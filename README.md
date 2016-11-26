# popctn
使用python 编写的一个动态伸缩小程序。
前端使用haproxy做负载均衡，‘看门狗’程序轮训所有容器的性能（CPU和mem），当达到一定值时，可以起新的容器。
新容器起来之后执行一段python程序发送自己的IP地址给server端，server端收到请求更改haproxy的配置文件，重启ha。
![image](https://github.com/wangxuan9237/popctn/blob/master/ha.jpg)

问题:
如果阈值降下来，需要回收容器，但怎么在容器退出时也发送一段内容到server端？
其实这种场景下使用zookeeper很合适。
