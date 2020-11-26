import socket

from SPECsocket.utils import run_onetime
from SPECsocket.utils.ssh import *

if __name__ == '__main__':
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
    cpu_init_nums = 32

    # 初始化服务器cpu的频率：将其调整到最高
    cpu_init(host, cpu_init_nums)

    # 获取各个CPU的可用频率：
    # CPU可调节的频率（KHZ）:[1801000, 1800000, 1700000, 1600000, 1500000, 1400000, 1300000, 1200000,
    # 1100000, 1000000,900000, 800000]
    cpu_freq = get_cpu_freq(host)

    # 查看当前的核心数
    cpu_data = get_cpu_info(host)
    cpu_number = int(cpu_data['cpu_number'])

    sleep(2)
    # 关闭ssh连接
    host.close()
    # 记录总共执行的轮数
    flag = 1
    # for num in range(0, cpu_number):
    for num in range(0, 32):
        # 逐个遍历不同的CPU的各个频率，由高到低

        # 为了恢复中途打断的执行,也可以是第一次执行
        if num == 0:
            for freq_num in range(1, len(cpu_freq)):
                print("=========================" + "第 " + str(flag) + "次的工况信息=========================")
                # 打印当前时间
                time_stamp = datetime.datetime.now()
                print("本次测试开始时间为：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
                sleep(3)

                # 给不同的cpu设置可用的频率
                modify_cpu_frequency(sut_ip, username, passwd, num, cpu_freq[freq_num], freq_num, flag)
                # 记录总共执行次数
                flag = flag + 1
                # 运行一次完整的程序
                run_onetime(sut_ip, port)

        else:
            for freq_num in range(2, len(cpu_freq)):
                print("=========================" + "第 " + str(flag) + "次的工况信息=========================")
                # 打印当前时间
                time_stamp = datetime.datetime.now()
                print("本次测试开始时间为：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))

                # 给不同的cpu设置可用的频率
                modify_cpu_frequency(sut_ip, username, passwd, num, cpu_freq[freq_num], freq_num, flag)
                # 记录总共执行次数
                flag = flag + 1
                # 运行一次完整的程序
                run_onetime(sut_ip, port)
                sleep(20)
        if num != cpu_number - 1:
            print("关闭CPU" + str(num) + "\n")
            shutdown_cpu(sut_ip, username, passwd, num)
    print("一共执行了" + str(flag) + "次")
