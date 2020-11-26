# 服务端
import socket
import threading
import time


# 创建新进程（线程）
def udplink(sock, message, addr):
    print('Accept new connection from %s:%s...' % addr)
    # 发送欢迎指令
    sock.sendto(b'Welcome!', addr)
    print('收到来自 ' + str(addr) + '的消息：' + message)
    while True:
        time.sleep(1)
        if not message or message.decode('utf-8') == 'exit':
            break
        reply = b'Hello, %s!' % message, addr
        sock.sendto(reply.encode('utf-8'), addr)
        # sock.sendto(b'Hello, %s!' % message, addr)

    sock.close()
    print('Connection from %s:%s closed.' % addr)


# from severSocket.cpu import *

# 这里的ip地址填本机的ip地址
# ip_port = ('192.168.1.103', 6899)

# 获取本地主机ip
hostname = socket.gethostname()
port = 8089
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
serverSocket.bind((hostname, port))
# flag = -1
# mark = -1
print('成功在sever端开启UDP服务' + str((hostname, port)))
print('Waiting for connection...')
while True:
    # 接收客户端发来的消息,建立新的连接
    message, addr = serverSocket.recvfrom(1024)
    # 创建新线程来处理UDP连接:
    t = threading.Thread(target=udplink, args=(serverSocket, message, addr))
    t.start()
# 关闭服务器，不可达
serverSocket.close()

#
# print('收到来自 ' + str(addr) + '的消息：' + message)
# if message == "state":
#     flag = os.popen('ps -ef | grep -i "runssj.sh"  | grep -v "grep" | wc -l').read().strip()
#     if int(flag) == 0 & mark == -2:
#         print("捕获到runssj程序运行结束")
#         reply = 'finish'
#         serverSocket.sendto(reply.encode('utf-8'), addr)
#         mark = -1
#     else:
#         reply = '当前的runssj执行状态是：flag=' + str(flag) + "  mark=" + str(mark)
#         serverSocket.sendto(reply.encode('utf-8'), addr)
# elif message == "runssj":
#     cmd = './runssj.sh'
#     if mark != -2:
#         flag = os.popen('ps -ef | grep -i "runssj.sh"  | grep -v "grep" | wc -l').read().strip()
#         if int(flag) > 0:
#             # 关闭多余的runssj
#             os.system('ps -ef | grep -i "runssj"| grep -v grep | awk {print $2} | xargs kill -9')
#             print("关闭多余的runssj")
#         reply = '开始执行runssj.sh'
#         # shell = 'nohup ./runssj.sh >out.txt 2>&1 &'
#         serverSocket.sendto(reply.encode('utf-8'), addr)
#         proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='/SPECpower_ssj2008/ssj/')
#         lines = proc.stdout.read().decode().strip()
#         print(lines)
#         # print(cmd)
#         print(reply)
#         # 执行一次mark,就会设置为-2标志
#         mark = -2
#     else:
#         reply = 'runssj已经在运行'
#         serverSocket.sendto(reply.encode('utf-8'), addr)
# elif message == "runtest":
#     # 测试案例，可以检测到结束
#     # reply = os.popen('/root/testshell.sh').read().strip()
#     proc = subprocess.Popen('/root/testshell.sh', stdout=subprocess.PIPE)
#     for line in proc.stdout.readlines():
#         line = line.decode().strip()
#         print(line)
#         sleep(2)
#         serverSocket.sendto(line.encode('utf-8'), addr)
#         if line == "finish":
#             print("okk")
# elif message == "exit":
#     reply = '客户端主动断开连接！'
#     serverSocket.sendto(reply.encode('utf-8'), addr)
#     print("客户端主动断开连接！")
# elif message == "terminateSeverProcess":
#     reply = '======服务端退出====='
#     serverSocket.sendto(reply.encode('utf-8'), addr)
#     print("======服务端退出=====")
#     break
# elif int(flag) == 0 & mark == -2:
#     print("捕获到runssj程序运行结束")
#     mark = -1
#     reply = 'finish'
#     serverSocket.sendto(reply.encode('utf-8'), addr)
# elif message == "receivedFinish":
#     print("客户端已经确认结束，开始清理现场")
#     flag = -1
#     mark = -1
# else:
#     reply = '已收到消息, %s!' % message
#     serverSocket.sendto(reply.encode('utf-8'), addr)
# flag = os.popen('ps -ef | grep -i "runssj.sh"  | grep -v "grep" | wc -l').read().strip()
