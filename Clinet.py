# -*- coding:utf-8-*-
import socket
import socket
import sys
# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host = socket.gethostname()
# 设置端口号
port = 9999
# 连接服务，指定主机和端口
s.connect((host, port))
content = "今年两会中，家庭教育话题持续高温。朋友圈流传的各种段子和文章，让“焦虑”成了中国父母的集体画像。"
# 接收小于 1024 字节的数据
s.sendall(content.encode('utf-8'))
msg = s.recv(1024)
s.close()
print (msg.decode('utf-8'))
