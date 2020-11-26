# 客户端
import socket

from utils.run_onetime import run_onetime
from utils.ssh import *


def runOneRound():
    # 获取本地主机
    hostname = socket.gethostname()

    # 指定远程sut服务ip和端口
    sut_ip = '192.168.10.100'
    port = 8088
    # 指定远程sut服务的root用户和密码
    username = 'root'
    passwd = 'root123'

    # 连接ssh:此处需要修改， 传入Ip，用户名，密码
    host = Ssh(sut_ip, username, passwd)

    # 可用cpu总数，这里是自己知道，可以写方法来调用
    # cpu_init_nums = 32

    # 初始化服务器cpu的频率：将其调整到最高
    # cpu_init(host, cpu_init_nums)

    # 获取各个CPU的可用频率：
    # CPU可调节的频率（KHZ）:[1801000, 1800000, 1700000, 1600000, 1500000, 1400000, 1300000, 1200000,
    # 1100000, 1000000,900000, 800000]
    # cpu_freq = get_cpu_freq(host)

    # 查看当前的核心数
    cpu_data = get_cpu_info(host)
    cpu_number = int(cpu_data['cpu_number'])

    sleep(2)
    # 关闭ssh连接
    host.close()
    flag = 1

    # 执行一次测试
    print("=========================" + "第 " + str(flag) + "次的工况信息=========================")
    # 打印当前时间
    time_stamp = datetime.datetime.now()
    print("本次测试开始时间为：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
    sleep(3)

    # 运行一次完整的程序
    run_onetime(sut_ip, port)


# 执行一次
runOneRound()
