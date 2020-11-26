import os

# 执行runtemp.sh
from time import sleep

runtemp_cmd = "cd /opt/SPECpower/PTDaemon; gnome-terminal -t \"runtemp\" -x bash -c \"sh " \
              "/opt/SPECpower/PTDaemon/runtemp.sh;exec bash;\" "

# 执行runpower.sh
runpower_cmd = "cd /opt/SPECpower/PTDaemon; gnome-terminal -t \"runpower\" -x bash -c \"sh " \
               "/opt/SPECpower/PTDaemon/runpower.sh;exec bash;\" "

rundirector_cmd = "cd /opt/SPECpower/ssj; gnome-terminal -t \"rundirector\" -x bash -c \"sh " \
                  "/opt/SPECpower/ssj/rundirector.sh;exec bash;\" "

rundirector_cmd = "cd /opt/SPECpower/ssj; gnome-terminal -t \"rundirector\" -x bash -c \"sh " \
                  "/opt/SPECpower/ssj/rundirector.sh;exec bash;\" "
runCCS_cmd = "cd /opt/SPECpower/ccs; gnome-terminal -t \"runCCS\" -x bash -c \"sh " \
             "/opt/SPECpower/ccs/runCCS.sh;exec bash;\" "
# 关闭所有打开的与“run”有关的bash终端
shutdown_cmd = "ps -ef | grep -i \"run\"|grep bash | grep -v grep | awk '{print $2}'|xargs kill -9"

os.system(runpower_cmd)
sleep(2)
os.system(runtemp_cmd)
sleep(2)
os.system(rundirector_cmd)
sleep(5)
os.system(runCCS_cmd)
sleep(2)

os.system(shutdown_cmd)
