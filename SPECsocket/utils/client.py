# 客户端
import socket

from time import sleep


class Client(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 建立连接
        self.clientSocket.connect((ip, port))

    def print(self):
        # 打印接收数据:
        print(self.clientSocket.recv(1024).decode('utf-8'))

    def send(self, message):
        # 向服务器发送消息，使用socket时，只能以字节形式传送，故需要encode()
        self.clientSocket.send(message.encode())

    def recv(self):
        # 接收服务器返回的消息和地址
        reply = self.clientSocket.recv(1024).decode('utf-8')
        return reply

    def close(self):
        # 关闭连接
        self.clientSocket.close()


def poll(hostname, port):
    '''
    向服务器询问程序是否还在运行
    :param hostname:
    :param port:
    :return:
    '''
    clientSocket = Client(hostname, port)
    clientSocket.send("IsExsit")

    # 接收服务器返回的消息和地址
    reply = clientSocket.recv()

    if reply == "finish":
        clientSocket.send('receivedFinish')
        # 发送确认接受到结束的信号信号
        # print("确认程序结束，发送结束信号")
        sleep(5)
    elif reply == "Running":
        sleep(3)
        # 再次接受信号
        reply2 = clientSocket.recv()
        print(reply2 + ";结束本次问询")
        # 发送确认接受到结束的信号信号
        # 发送结束信号
        clientSocket.send("exit")

    else:
        print(reply)
        # 发送结束信号
        clientSocket.send("exit")
        sleep(5)

    clientSocket.close()
    return reply

# # 测试程序
# if __name__ == '__main__':
#     hostname = socket.gethostname()
#     # ip='192.168.1.103'
#     port = 8088
#     # 创建一个socket
#     clientSocket = Client(hostname, port)
#
#     # # 打印服务器发来的欢迎连接的数据:
#     # print(clientSocket.recv())
#     # flag = False
#
#     sleep(1)
#     # 向服务器发送执行的消息
#     clientSocket.send("runtest")
#
#     # 接收服务器返回的消息和地址
#     reply = clientSocket.recv()
#     # 打印接受的数据
#     print(reply)
#
#     # 发送结束信号
#     clientSocket.send("exit")
#     sleep(4)
#
#     # 关闭连接
#     clientSocket.close()
#     print("--------向服务器发送问询信号--------")
#     while True:
#         sleep(10)
#         # print("--------向服务器发送问询信号--------")
#         reply = poll(hostname, port)
#
#         if reply == "finish":
#             # 发送确认接受到结束的信号信号
#             print("------确认程序结束，发送结束信号------")
#             sleep(5)
#             break

# if reply == "Running":
#     flag = True
#     sleep(3)
#     # 再次接受信号
#     reply = clientSocket.recv()
#     print(reply + ";结束本次问询")
#     # 发送确认接受到结束的信号信号
#     clientSocket.send('receivedRunning')
#     sleep(5)
#     break

# # 退出客户端
# if message == "exit":
#     # 发送结束信号
#     clientSocket.send('exit')
#     sleep(5)
#     break
