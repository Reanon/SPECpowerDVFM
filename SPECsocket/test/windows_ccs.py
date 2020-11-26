import os  # 导入OS模块
import time


def runpower():
    # 停顿一秒
    time.sleep(5)
    # 调用初始化功率分析仪
    # os.system('start ./SPECpower/PTDaemon/runpower.bat')
    os.system('start  callRunpower.bat')


def runtemp():
    # 停顿一秒
    time.sleep(5)
    # 调用温度传感器 os.system('start C:/SPECpower/PTDaemon/runtemp.bat')
    os.system('start  callRuntemp.bat')


def stopRunpower():
    # 停顿一秒
    time.sleep(5)
    # 调用初始化功率分析仪
    # os.system('start ./SPECpower/PTDaemon/runpower.bat') TASKKILL /F /FI "WINDOWTITLE eq 运行*"
    mes = os.popen('TASKKILL /F /IM cmd.exe /T')
    print(mes)


def stopRuntemp():
    # 停顿一秒
    time.sleep(5)
    # 调用温度传感器 os.system('start C:/SPECpower/PTDaemon/runtemp.bat')
    # os.system('taskkill /f  callRuntemp.bat')
    os.system('taskkill /FI "WINDOWTITLE eq callRuntemp.bat" /IM cmd.exe /F ')


def rundirector():
    # 停顿一秒
    time.sleep(5)
    # 调用 rundirector
    os.system('start callRundirector.bat')


def runCCS():
    # 停顿一秒
    time.sleep(5)
    # 调用runCCS
    # os.system('start C:/SPECpower/ccs/runCCS.bat')
    os.system('start callRunCCS.bat')


def stopRunCCS():
    # 停顿一秒
    time.sleep(5)
    # 调用runCCS
    # os.system('start C:/SPECpower/ccs/runCCS.bat') baititle 1.bat
    # os.system('stop callRunCCS.bat')
    os.system('stop callRunCCS.bat')


def stopRundirector():
    # 停顿一秒
    time.sleep(5)
    # 调用 rundirector
    os.system('stop callRundirector.bat')


def stopALL():
    # 停顿一秒
    time.sleep(5)
    # 关闭所有cmd 窗口
    os.system('TASKKILL /F /IM cmd.exe /T')


def runVAM():
    # 停顿一秒
    time.sleep(5)
    # 调用runVAM
    os.system('start callRunVAM.bat')

#
# # 测试
# runtemp()
# runpower()
# stopALL()
# # rundirector()
# # runCCS()
# # runVAM()
