import datetime
from time import sleep

from utils.ssh import Ssh


def get_cpu_info(host):
    out_list = []
    cpu_data = {}
    cmd_list = [
        "cat /proc/cpuinfo |grep 'model name' -m 1|awk -F: '{print $2}'",
        "cat /proc/cpuinfo |grep 'cpu MHz' -m 1|awk -F: '{print $2}'",
        "cat /proc/cpuinfo |grep 'processor' | wc -l",
        "cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"
    ]

    for cmd in cmd_list:
        # 读取命令行，并且将输出存入data中
        # data = os.popen(cmd).read().strip()
        result = host.send(cmd)
        out_list.append(result)

    cpu_data["cpu_model"] = out_list[0]
    cpu_data["cpu_rate"] = out_list[1]
    cpu_data["cpu_number"] = out_list[2]
    cpu_data["cpu_max_freq"] = out_list[3]

    return cpu_data


def get_cpu_freq(host):
    '''
    读取CPU_Freq：读取可用的CPU频率，
    待完成：将各个cpu的频率分别存放，外面直接调用。
    :return:
    '''
    out_list = []
    freq_data = {}
    cmd_list = [
        # 读取可用的Cpu频率
        'cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies',
    ]

    for cmd in cmd_list:
        # 读取命令行，并且将输出存入data中
        # data = os.popen(cmd).read().strip()
        data = host.send(cmd)
        # out_list.append(data)

    # freq_data["cpu_freq"] = out_list[0]
    # 将读取出来的可用频率转化为list
    freq_data = list(map(int, data.split()))
    return freq_data


def print_cpu_info(host):
    '''
    打印cpu的信息

    :return:
    '''
    # 查看当前的核心数
    cpu_data = get_cpu_info(host)
    # 获取各个CPU的可用频率
    cpu_freq = get_cpu_freq(host)
    cpu_number = int(cpu_data['cpu_number'])
    cpu_rate = float(cpu_data['cpu_rate'])
    cpu_model = cpu_data['cpu_model']
    cpu_max_freq = cpu_data["cpu_max_freq"]

    sleep(2)
    # 显示处理器的性能
    print("CPU型号:", cpu_model)
    print("CPU最高频率:", cpu_max_freq, "KHZ")
    print("CPU逻辑个数:", cpu_number)
    print("CPU可调节的频率（KHZ）：", cpu_freq)


def modify_cpu_frequency(ssh_ip, username, passwd, cpu_num, frequency, freq_num, flag=1, upper=-1, lower=-1):
    """
    修改CPU的频率,不再依赖ssh

    :param cpu_num:总共的CPU数目
    :param frequency:
    :param upper:
    :param lower:
    :return:
    """
    sleep(1)
    # 此处需要修改， 传入Ip，用户名，密码
    # host = Ssh('192.168.1.103', 'root', 'teamwork@123')
    host = Ssh(ssh_ip, username, passwd)
    sleep(1)

    # 打印频率调节信息
    print("--------------" + "当前调节到cpu" + str(cpu_num) + "的第" + str(freq_num) + "级频率：" + str(frequency) +
          "KHZ--------------")

    # 执行频率调节命令
    print(host.send('cpupower --cpu ' + str(cpu_num) + ' frequency-set --freq ' + str(frequency) + 'KHz'))
    # 打印出当前各个cpu的频率
    print(host.send("cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_cur_freq"))
    print("\n ")

    sleep(2)
    # 关闭ssh连接
    host.close()


def shutdown_cpu(ssh_ip, username, passwd, num):
    sleep(1)
    # 此处需要修改， 传入Ip，用户名，密码
    # host = Ssh('192.168.1.103', 'root', 'teamwork@123')
    # host = Ssh('192.168.31.244', 'root', 'ssl123456')
    host = Ssh(ssh_ip, username, passwd)

    sleep(2)

    host.send("echo \'0\' " + " > /sys/devices/system/cpu/cpu" + str(num) + "/online")

    sleep(2)

    # 关闭ssh连接
    host.close()


def cpu_init(host, cpu_total_nums):
    # 设置工作模式到userspace
    host.send("cpupower frequency-set -g userspace")

    # 开启所有cpu
    print("开所有cpu,并且将它们的频率设置为最高")
    for num in range(0, cpu_total_nums):
        # echo 1 > /sys/devices/system/cpu/cpu1 online
        host.send("echo \'1\' " + " > /sys/devices/system/cpu/cpu" + str(num) + "/online")

    # 得到cpu最大的频率
    cpu_max_freq = host.send("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
    # 给不同的cpu设置可用的的最大频率
    for cpu_num in range(0, cpu_total_nums):
        host.send('cpupower --cpu ' + str(cpu_num) + ' frequency-set --freq ' + str(cpu_max_freq) + 'KHz')
        # modify_cpu_frequency(num, cpu_max_freq)

    # 打印cpu的各类信息
    print_cpu_info(host)
    sleep(1)
    # 打印出当前各个cpu的频率
    print("=================================" + "第 " + str(1) + "次的工况信息=================================")
    # 打印当前时间
    time_stamp = datetime.datetime.now()
    print("本次测试开始时间为：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
    # print(host.send("cat /proc/cpuinfo | grep -i mhz"))
    print(host.send("cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_cur_freq"))
