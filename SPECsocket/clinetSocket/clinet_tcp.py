# 客户端
import socket

from time import sleep

# 获取本地主机
hostname = socket.gethostname()

# 指定远程服务ip
ip = '192.168.10.100'
port = 8088

# 创建一个socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 建立连接:连接本地(hostname, port)，连接远程(ip, port)
clientSocket.connect((ip, port))

# # 打印接收数据:
# print(clientSocket.recv(1024).decode('utf-8'))
# flag = False
while True:
    # 提示输入消息
    message = input('发送的消息：').strip()
    # 向服务器发送消息，使用socket时，只能以字节形式传送，故需要encode()
    clientSocket.send(message.encode())
    sleep(4)
    # 接收服务器返回的消息和地址
    reply = clientSocket.recv(1024).decode('utf-8')
    # 打印接受的数据
    print(reply)
    if reply == "finish":
        flag = True
        clientSocket.send(b'receivedFinish')
        # 发送确认接受到结束的信号信号
        print("确认程序结束，发送结束信号")
        sleep(5)
        break

    # 退出客户端
    if message == "exit":
        # 发送结束信号
        clientSocket.send(b'exit')
        sleep(5)
        break

# 关闭连接
clientSocket.close()
