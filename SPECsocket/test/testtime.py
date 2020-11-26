import datetime

# 打印当前时间
time_stamp = datetime.datetime.now()
print("本次测试时间为：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
cpu_freq = [1801000, 1800000, 1700000, 1600000, 1500000, 1400000, 1300000, 1200000, 1100000, 1000000, 900000, 800000]
cpu_number = 32
flag = 14
for num in range(1, 32):
    # 逐个遍历不同的CPU的各个频率，由高到低
    # for freq_num in range(2, len(cpu_freq) - 1):
    # 只是为了更快地测试
    # 为了恢复中途打断的执行
    if num == 1:
        for freq_num in range(5, len(cpu_freq)):
            print("========================" + "第 " + str(flag) + "次的工况信息========================")

            # 打印频率调节信息
            print("---------------" + "当前调节到cpu" + str(num) + "的第" + str(freq_num) + "级频率：" + str(
                cpu_freq[freq_num]) + "KHZ---------------")
            # 记录总共执行次数
            flag = flag + 1
    else:
        for freq_num in range(2, len(cpu_freq)):
            print("========================" + "第 " + str(flag) + "次的工况信息========================")

            print("---------------" + "当前调节到cpu" + str(num) + "的第" + str(freq_num) + "级频率：" + str(
                cpu_freq[freq_num]) + "KHZ---------------")
            # 记录总共执行次数
            flag = flag + 1

    if num != cpu_number - 1:
        print("关闭CPU" + str(num) + "\n")
