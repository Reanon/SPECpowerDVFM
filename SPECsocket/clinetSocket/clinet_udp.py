# 客户端
import socket

# ip_port = ('192.168.1.103', 6899)

# 获取本地主机ip
hostname = socket.gethostname()
port = 8089
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

while True:
    message = input('发送的消息：').strip()
    # 向服务器发送消息，使用socket时，只能以字节形式传送，故需要encode()
    clientSocket.sendto(message.encode(), (hostname, port))
    # 接收服务器返回的消息和地址
    reply = clientSocket.recv(1024).decode('utf-8')
    print(reply)
    # 输入exit 退出程序
    if message == 'exit':
        # 发送结束信号
        clientSocket.send(b'exit')
        break

# 关闭连接
clientSocket.close()
