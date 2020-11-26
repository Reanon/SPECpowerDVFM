r"""
在服务端本地执行的程序调节cpu的程序

"""
import os


#

def get_cpu_info():
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
        data = os.popen(cmd).read().strip()
        out_list.append(data)

    cpu_data["cpu_model"] = out_list[0]
    cpu_data["cpu_rate"] = out_list[1]
    cpu_data["cpu_number"] = out_list[2]
    cpu_data["cpu_max_freq"] = out_list[3]
    return cpu_data


def get_cpu_freq():
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
        data = os.popen(cmd).read().strip()
        # out_list.append(data)

    # freq_data["cpu_freq"] = out_list[0]
    # 将读取出来的可用频率转化为list
    freq_data = list(map(int, data.split()))
    return freq_data


def modify_cpu_frequency(cpu_num, frequency, upper=-1, lower=-1):
    """
    修改CPU的频率
    :param cpu_num:总共的CPU数目
    :param frequency:
    :param upper:
    :param lower:
    :return:
    """
    # 执行频率调节命令
    print(os.popen('cpupower --cpu ' + str(cpu_num) + ' frequency-set --freq ' + str(frequency) + 'KHz').read())

    print("将" + "CPU" + str(cpu_num) + "的频率修改为:" + str(frequency) + "KHZ")


def cpu_init():
    # 打印cpu的各类信息
    # print_cpu_info()

    # 可用cpu总数，这里是自己知道，可以写方法来调用
    cpu_total_nums = 4

    # 开启所有cpu
    print("开所有cpu,并且将它们的频率设置为最高")
    for num in range(0, cpu_total_nums):
        # echo 1 > /sys/devices/system/cpu/cpu1 online
        os.system("echo \'1\' " + " > /sys/devices/system/cpu/cpu" + str(num) + "/online")

    # 得到cpu最大的频率
    cpu_max_freq = os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq").read().strip()
    for num in range(0, cpu_total_nums):
        # 给不同的cpu设置可用的的最大频率
        modify_cpu_frequency(num, cpu_max_freq)

    # 打印出当前各个cpu的频率
    os.system("cat /proc/cpuinfo | grep -i mhz")


def print_cpu_info():
    '''
    打印cpu的信息
    :return:
    '''
    # 查看当前的核心数
    cpu_data = get_cpu_info()
    # 获取各个CPU的可用频率
    cpu_freq = get_cpu_freq()
    cpu_number = int(cpu_data['cpu_number'])
    cpu_rate = float(cpu_data['cpu_rate'])
    cpu_model = cpu_data['cpu_model']
    cpu_max_freq = cpu_data["cpu_max_freq"]

    # 显示处理器的性能
    print("CPU型号:", cpu_model)
    print("CPU最高频率:", cpu_max_freq, "KHZ")
    print("CPU逻辑个数:", cpu_number)
    print("CPU可调节的频率（KHZ）：", cpu_freq)
    # reply = "CPU型号:" + str(cpu_model) + "\nCPU最高频率:" + str(cpu_max_freq) + "KHZ" + "\nCPU逻辑个数:" \
    #         + str(cpu_number) + "\nCPU可调节的频率（KHZ）：" + str(cpu_freq)
    # return reply


def cpu_state():
    print(os.system("cat /proc/cpuinfo | grep -i mhz"))
