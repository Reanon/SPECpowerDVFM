import os

from time import sleep


def stopALL():
    '''
    关闭所有打开的与“run”有关的bash终端
    :return:
    '''
    shutdown_bash = "ps -ef |grep bash | grep -v grep | awk '{print $2}'|xargs kill -9"
    # shutdown_cmd2 = "ps -ef |grep bash |grep ssj| grep -v grep | awk '{print $2}'|xargs kill -9"
    os.system(shutdown_bash)
    # os.system(shutdown_cmd2)


def runpower():
    '''
        在控制端运行runpower.bat
    :return:
    '''
    sleep(2)
    runpower_cmd = "cd /opt/SPECpower/PTDaemon; gnome-terminal -t \"runpower\" -x bash -c \"sh " \
                   "/opt/SPECpower/PTDaemon/runpower.sh;exec bash;\" "
    os.system(runpower_cmd)


def runtemp():
    '''
    在控制端下点击runtemp.bat
    :return:
    '''
    sleep(2)
    runtemp_cmd = "cd /opt/SPECpower/PTDaemon; gnome-terminal -t \"runtemp\" -x bash -c \"sh " \
                  "/opt/SPECpower/PTDaemon/runtemp.sh;exec bash;\" "

    os.system(runtemp_cmd)


def rundirector():
    '''
    # 在控制端下点击rundirector.bat

    :return:
    '''
    sleep(3)
    rundirector_cmd = "cd /opt/SPECpower/ssj; gnome-terminal -t \"rundirector\" -x bash -c \"sh " \
                      "/opt/SPECpower/ssj/rundirector.sh;exec bash;\" "
    os.system(rundirector_cmd)


def runCCS():
    '''
    # 在控制端运行runCCS.bat
    :return:
    '''
    sleep(5)
    runCCS_cmd = "cd /opt/SPECpower/ccs; gnome-terminal -t \"runCCS\" -x bash -c \"sh " \
                 "/opt/SPECpower/ccs/runCCS.sh;exec bash;\" "
    os.system(runCCS_cmd)