# 服务端
import os
import socket
import threading
from time import sleep


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # 发送欢迎指令
    # sock.send(b'Welcome!')
    while True:
        # 接受来自客户端的消息
        message = sock.recv(1024).decode('utf-8')
        # 打印来自客户端的消息
        print('收到来自 ' + str(addr) + '的消息：' + message)
        sleep(1)
        # 处理消息
        if message == 'exit' or message == "receivedFinish":
            print("接收到关闭信号")
            break
        else:
            handle_message(sock, message)

    # 关闭连接
    sock.close()
    print(' 来自 %s:%s 的连接关闭.' % addr)


def handle_message(sock, message):
    '''
     针对不同事务，进行不同的消息处理
    :return:
    '''

    if message == "runssj":
        # 测试案例，可以检测到结束
        print("===================开始执行测试runssj=================")
        sleep(1)
        ssj_cmd = "cd /opt/SPECpower/ssj; gnome-terminal -t \"runssj\" -x bash -c \"sh " \
                   "/opt/SPECpower/ssj/runssj.sh;exec bash;\" "
        os.system(ssj_cmd)
        sleep(1)
        ppid = os.popen('ps -ef | grep -i runssj|grep bash | grep -v grep | awk \'{print $2} \'').read().strip()
        reply = '服务器开始执行测试runtest;进程号是 %s' % ppid
        sock.send(reply.encode('utf-8'))

    elif message == "terminateSeverProcess":
        reply = '======服务端退出====='
        sock.send(reply.encode('utf-8'))
        print("======服务端退出=====")
        # break
    elif message == "receivedFinish":
        print("客户端已经确认结束，开始清理现场")
    elif message == "IsExsit":
        flag = os.popen('ps -ef | grep bash |grep -i runssj | grep -v grep | wc -l').read().strip()
        if int(flag) == 0:
            print("程序运行结束")
            reply = 'finish'
            sock.send(reply.encode('utf-8'))
        else:
            ppid = os.popen('ps -ef | grep -i runssj |grep bash | grep -v grep | awk \'{print $2} \'').read().strip()
            print('程序还在运行,进程号是 %s' % ppid)
            # 发送程序还在运行的信号
            reply = "Running"
            # reply = '程序还在运行,进程号是 %s' % ppid
            sock.send(reply.encode('utf-8'))
            sleep(3)
            reply = '程序还在运行,进程号是 %s' % ppid
            sock.send(reply.encode('utf-8'))


    else:
        sock.send(('sever已接受: %s!' % message).encode('utf-8'))
        print("=====消息处理完毕=====")
        # reply = '已收到消息, %s!' % message
        # serverSocket.sendto(reply.encode('utf-8'), addr)


# 这里的ip地址填本机的ip地址
hostname = socket.gethostname()

# 指定远程服务ip
ip = '192.168.10.100'

port = 8088
# 创建一个socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
serverSocket.bind((ip, port))

print('成功在sever端开启TCP服务' + str((ip, port)))

# 开始监听端口，传入的参数指定等待连接的最大数量
serverSocket.listen(5)
print('Waiting for connection...')
while True:
    # 接受一个TCP新连接:
    sock, addr = serverSocket.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

# 关闭服务器，不可达
serverSocket.close()
