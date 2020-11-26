import datetime

from SPECsocket.utils.ccs import *
from SPECsocket.utils.client import *

def run_onetime(ip, port):
    # 关闭所有bash窗口
    stopALL()
    # 在控制端运行runpower.bat

    runpower()
    sleep(2)
    # 在控制端下点击runtemp.bat
    runtemp()
    sleep(2)
    # 在控制端下点击rundirector.bat
    rundirector()
    sleep(2)

    # 建立连接:连接本地(hostname, port)，连接远程(ip, port)
    clientSocket = Client(ip, port)

    sleep(5)
    # 向服务器发送执行的消息
    clientSocket.send("runssj")

    # 接收服务器返回的消息和地址
    reply = clientSocket.recv()
    # 打印接受的数据
    print(reply)

    # 发送结束信号
    clientSocket.send("exit")
    sleep(5)

    # 关闭连接
    clientSocket.close()

    sleep(3)
    # 在控制端运行runCCS.bat
    runCCS()
    # 设置询问时间
    timeout = 120

    print("----------------向服务器发送问询信号，每隔" + str(timeout) + "s问询一次" + "----------------")
    while True:
        sleep(timeout)
        # print("--------向服务器发送问询信号--------")
        reply = poll(ip, port)

        if reply == "finish":
            # 发送确认接受到结束的信号信号
            print("-------------------确认程序结束，发送结束信号-------------------")
            sleep(5)
            break

    sleep(20)
    # 关闭所有bash 窗口
    stopALL()

    # 打印当前时间
    time_stamp = datetime.datetime.now()
    print("本次测试结束时间为：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
    print("=============================结束本次运行=============================\n")


if __name__ == '__main__':
    # 指定远程sut服务ip和端口
    sut_ip = '192.168.10.100'
    port = 8088

    # 运行一次完整的程序
    run_onetime(sut_ip, port)
