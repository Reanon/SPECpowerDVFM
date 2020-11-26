# SPECpower_ssj2008 操作指南

## 使用说明

第零节简单介绍了本软件的情况，包括各个部件的基本信息。第一节是对各个文件的配置说明。快速执行可以参照第三节的"操作流程"，其中包含各个文件的启动顺序。第四节是详细的配置文档。第五节是实验日志。不同服务器的性能不同，一次运行大约持续两个小时。

## 零、组织结构

### 0.1 软件组成

#### 服务器端Java（SSJ）–工作负载

Server Side Java 是一个Java程序，旨在测试CPU，高速缓存，内存，共享内存处理器的可伸缩性，JVM（Java虚拟机）实现JIT（Just In Time）编译器，垃圾收集以及待测试操作系统的其他方面功能。

#### 功率和温度守护程序（PTDaemon）

Power and Temperature Daemon (PTDaemon)将在测量间隔期间将控制 功率分析仪 或 温度传感器 的工作分担给待测试系统以外的系统。

#### 控制和收集系统

Control and Collect System (CCS),包括Visual Activity Monitor（VAM）

- CCS是一个多线程Java应用程序，它控制并允许来自多个数据源的数据的协调收集，例如在单独的SUT（被测系统）上运行的工作负载，电源分析器和温度传感器。
- VAM是一个软件包，旨在结合SPECpower_ssj2008基准同时显示一个，两个或三个待测试系统的活动。

### 硬件组成

#### Server Under Test (SUT)

SUT是由SSJ（服务侧java）工作负载驱动的系统。 SUT的性能和功耗特性将通过基准进行捕获和测量。

#### Power Analyzer

这里采用的功耗分析仪为[PA1000](https://www.tek.com.cn/power-analyzer/pa1000)，其有中文用户手册。

##### 下载驱动

如果有不懂的操作可以在[Tektronix官网](https://www.tek.com.cn/)询问客服，可以联系客服下载驱动和一些相关的技术问题。

功率分析仪用于测量和记录SUT消耗的功率。这里采用的是[PA1000](http://www.tek.com/power-analyzer/pa1000)，首先在官网上需要下载驱动[TEKVISA Connectivity Software - V4.2.0](https://www.tek.com.cn/oscilloscope/tds7054-software/tekvisa-connectivity-software-v420)。

端口选择

```shell
 ./ptd-linux-x86 -p 8888 56 /dev/usbtmc0
```

##### 固定量程

#### Temperature Sensor

温度传感器用于捕获对SUT进行基准测试的环境的温度。这里采用**1-wire温度传感器**（[USB9097](http://pcsensor.com/1-wire-adapter/usb9097.html) + [DS18B20](http://pcsensor.com/1-wire-series/temperature-probe/dx.html)），主要由USB9097和Tx sensor组成，将温度传感器一端插入USB9097的**绿色接口**，然后USB插入电脑端口。下载[温度传感器驱动](https://www.pcsensor.cn/Resource20200118170246108_en.html)

1. 安装Driver里面的USB Driver；

2. 安装Driver里面的1 Wire Driver；(此文件夹中的程序属于Java程序，需要安装目录里支持Java的软件）

3. 安装setup.exe;（如果您的电脑没有装framework，安装过程中将自动跳到微软的官方网站自动安装framework，请不要中止framework的安装；如果您已经安装了framework，直接下一步就行）

4. 检查是否安装成功：“设备管理器”-观察“端口”地方的刷新，看看是否出现一个新的端口，如：`USB-SERIAL CH340 （COM 3）`，出现这种情况，证明您的USB驱动已经安装成功，如果没有出现这种情况，请重新安装USB  Driver.（出现的端口号不一定是COM3，也可能是其他编号，这个是正常现象）

   ![img](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200914145501.png)

打开安装好的TEPer1W软件，然后可以看到其已经正确。

![img](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200914145522.png)

#### Controller System

控制器系统是一个单独的系统，运行SPECpower_ssj2008基准测试套件的CCS和功率和温度后台驻留程序（PTD）部分。

![image-20200816211526384](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200829190740.png)

## 一、环境准备

控制系统（a system to control the test (Controller System)ip: 192.168.182.2

待测试系统（the system under test, or SUT)ip:192.168.182.130

### 1.1 安装Java

将jdk-8u251-linux-x64.tar.gz文件上传到linux的/opt/ 目录下，然后解压文件

```shell
tar -zxvf jdk-8u251-linux-x64.tar.gz
```

把解压出来的`jdk1.8.0_251`移动/usr/local 目录下

```shell
mv jdk1.8.0_251 /usr/local
```

配置profile文件

```shell
vim /etc/profile	
```

将以下几行添加到profile文件中

```shell
#定义java的环境变量
JAVA_HOME=/usr/local/jdk1.8.0_251
JRE_HOME=$JAVA_HOME/jre
CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
PATH=$JAVA_HOME/bin:$PATH

export JAVA_HOME
export JRE_HOME
export CLASSPATH
export PATH
```

使得修改的配置生效

```shell
source /etc/profile
```

使用`java -version`命令来验证自己Java的环境是否配置成功

![image-20200717205831039](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200829190741.png)

### 1.2 安装Anaconda3

下载可以在Anaconda官网上下载[Anaconda](https://www.anaconda.com/products/individual)或者在清华源上下载[Anaconda](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)，所使用的版本是[Anaconda3-2020.07-Linux-x86_64.sh](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2020.07-Linux-x86_64.sh).使用Xshell附带的Xftp,将安装包传入`/home/`目录下，安装Anaconda：

```shell
bash Anaconda3-2020.07-Linux-x86_64.sh
```

中途会让选择安装的路径，一般使用`/usr/local/anaconda3`就行了

```shell
Anaconda3 will now be installed into this location:
/root/anaconda3
  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below
[/root/anaconda3] >>> /usr/local/anaconda3
```

配置环境变量

1. 在命令行界面输入

```shell
vim /etc/profile
```

2. 进入编辑状态，然后输入

```shell
# PATH=/usr/bin/anaconda3/bin:$PATH
PATH=/usr/local/anaconda3/bin:$PATH
```

3. 回到命令行界面，使配置生效

```shell
[root@xxx]# source /etc/profile
[root@xxx]# python
Python 3.8.3 (default, Jul  2 2020, 16:21:59) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
# 按ctrl+Z退出
```

### 1.3 安装SPECpower_ssj2008

将SPECpower传输到 linux的opt 目录下，然后讲iso文件挂载到/mnt/目录下

```shell
[root@host]# mount -o loop /opt/SPECpower_ssj2008-1.12.iso  /mnt/
```

切换到mnt目录下`cd /mnt`，在当前目录下使用命令行模式安装：

```shell
java -jar setup.jar -i  console
```

会默认安装到根目录下的`/SPECpower_ssj200`

```
/opt/SPECpower
```

如果安装不上的话，也可以复制安装文件中的（(ccs, PTDaemon, ssj, images, and redistributable sources）到测试系统和控制系统里面。最好全部放置在创建的名为 `SPECpower_ssj2008`的目录下。

![image-20200717211857136](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200829190742.png)

### 1.4 网络配置

配置文件地址在`/etc/sysconfig/network-scripts` 目录下，有一个 `ifcfg-` 开头的几个配置文件。找到对应于`192.168.xxx.xxx`的文件

![image-20200922143545845](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200922143545.png)

修改配置文件 ，设置固定ip地址，下面的配置文件（Centos8中字符串没有引号）。

```shell
# 类型
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"

#是否启动DHCP：none为禁用DHCP;static为使用静态ip地址；设置DHCP为使用DHCP服务;如果要设定多网口绑定bond的时候，必须设成none。
BOOTPROTO="dhcp" 

#就是default route，是否把这个网卡设置为ipv4默认路由
DEFROUTE="yes"
# 如果ipv4配置失败禁用设备
IPV4_FAILURE_FATAL="no"
#是否使用IPV6地址：yes为使用；no为禁用
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
#就是default route，是否把这个网卡设置为ipv6默认路由
IPV6_DEFROUTE="yes"
# 如果ipv6配置失败禁用设备
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
#网络连接的名字
NAME=eno3
#唯一标识
UUID=74ec16ef-f741-4501-9ee0-8d7862d520ec
# 网卡名称
DEVICE=eno3 
#启动或者重启网络时是否启动该设备：yes是启用；no是禁用
ONBOOT="yes" 

```

`TYPE`、`BOOTPROTO`、`NAME`、`DEVICE`、`ONBOOT`、`IPV6INIT` 这些必须存在；`DNS1`、`IPADDR`、`GATEWAY`、`PREFIX`使用固定ip必须有这些配置。于是在上面的文件中添加如下配置信息：

```shell
# 将static为使用静态ip地址，并注释掉BOOTPROTO="dhcp"
BOOTPROTO="static"
# 采用谷歌的默认DNS服务器
DNS1=8.8.8.8       
# 子网掩码 RedHat，不同版本的Linux的配置是不一样的 
NETMASK=255.255.255.0 
#IP地址,填你的ip
IPADDR=192.168.10.100
#网关
GATEWAY=192.168.10.1                    
```

最后的配置文件结果

```shell
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DNS1=8.8.8.8
NETMASK=255.255.255.0
IPADDR=192.168.10.100
GATEWAY=192.168.10.1
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=eno3
UUID=74ec16ef-f741-4501-9ee0-8d7862d520ec
DEVICE=eno3
ONBOOT=yes
```

重启服务时，Centos8 可能会报错，可以参考下这篇[RHEL8和CentOS8怎么重启网络](https://my.oschina.net/lenglingx/blog/3223463)，这里使用`yum install network-scripts`来安装传统`的network.service`，然后重启网络服务。

```shell
# 重启网络服务
service network restart
```

将两个系统都连接到网络，并为每个系统的网络适配器提供一个不同的IP地址

- 控制系统CCS（a system to control the test)：192.168.10.101
- 待测试系统SUT（the system under test):192.168.10.100
- 验证两个系统都可以相互`ping [ip地址]`通。

```shell 
[root@localhost SPECpower_ssj2008]# ping 192.168.10.101
PING 192.168.10.101 (192.168.10.101) 56(84) bytes of data.
64 bytes from 192.168.10.101: icmp_seq=1 ttl=64 time=0.916 ms
...
# 按住ctrl+C 退出
```

可以通过`ifconfig`命令查看自己的ip地址。

## 二、编辑配置文件

### 2.1  CCS 控制端

电源和温度的守护进程（Power & Temperature Daemon，PTDaemon）

通过[SPEC PTDaemon™ Tool](https://www.spec.org/power/docs/SPECpower-Device_List.html)可以查到支持SPECpower_ssj2008的功耗仪和温度传感器列表。本实验使用的温度传感器是[USB9097](http://pcsensor.com/1-wire-adapter/usb9097.html) + [DS18B20](http://pcsensor.com/1-wire-series/temperature-probe/dx.html)；功耗仪使用的是[PA1000](http://www.tek.com/power-analyzer/pa1000)；

在CCS端首先需要使用[spec-updater](https://www.spec.org/power/docs/SPECpower-PTD-Update_Process.html)来更新`\SPECpower\PTDaemon`下的`ptd-windows-x86.exe`(`runpower.bat`和`runtemp.bat` 都会调用)

- 将下载好的[SPEC-updater v0.6 zip](http://www.spec.org/power/ptd_patches/SPEC-updater-0.6.zip)]在本地解压，然后将`ptd-windows-x86.exe`放入`\SPEC-updater\bin`目录下，打开`cmd`终端

  - ```shell
    # 切换到\SPEC-updater\bin目录下
    C:\Users\Reanon>cd C:\SPECpower\PTDaemon\SPEC-updater\bin
    # 更新ptd-windows-x86.exe 为 ptd-windows-x86new.exe
    C:\SPECpower\PTDaemon\SPEC-updater\bin>spec-updater update ptd-windows-x86.exe ptd-windows-x86new.exe
    # 使用ptd-windows-x86new.exe -h查找帮助文档
    C:\SPECpower\PTDaemon\SPEC-updater\bin>ptd-windows-x86new.exe -h
    ```

- 通过更新过的`ptd-windows-x86new.exe -h`可以看到以下查找到对应的功率分析仪和温度传感器型号的`Device type`

- ```
  Power Analyzer device types:
  
  for AC power measurements:
    0. *Dummy (testing only)             8. Yokogawa WT210
   14. Instek GPM-8212                  16. ZES LMG450:1-Channel
   17. ZES LMG450:4-Channel             18. ZES LMG500:1-Channel
   19. ZES LMG500:4-Channel             22. ZES LMG95
   23. Voltech PM1000+                  25. Infratek 107A-1
   28. Xitron 280X:1-Channel            31. Chroma 66202
   33. Hioki 3334                       35. Yokogawa WT500:1-Channel
   36. Yokogawa WT500:MULTIPHASE        37. ZES LMG450:3-Phase
   38. ZES LMG500:3-Phase               41. N4L PPA15X0:1-Channel
   44. N4L PPA55X0:1-Channel            47. Yokogawa WT1800:1-Channel
   48. Yokogawa WT500:MULTICHANNEL      49. Yokogawa WT310
   50. N4L PPA5X0:1-Channel             51. Chroma 66203 66204:1ch
   52. Yokogawa WT330:1-Channel         53. Yokogawa WT330:3-Phase
   56. **Tektronix PA1000                 57. Hioki PW3335
   58. Hioki PW3336:1-Channel           59. Hioki PW3336:2-Channel
   60. Hioki PW3337:1-Channel           61. Hioki PW3337:3-Channel
   62. Hioki PW3337:3-Phase             65. Chroma 66205
   66. Yokogawa WT5000:1-Channel        67. Yokogawa WT5000:3-Phase
  
  for DC power measurements:
   500. *DC Dummy (testing only)        508. DC Yokogawa WT210
   522. DC ZES LMG95                    535. DC Yokogawa WT500:1-Channel
   549. DC Yokogawa WT310               550. DC N4L PPA5X0:1-Channel
   551. DC Chroma 66203 66204:1ch       556. DC Tektronix PA1000
   557. DC Hioki PW3335                 565. DC Chroma 66205
   566. DC Yokogawa WT5000:1-Channel
  
  Temperature sensor device types:
   1000. *Dummy (testing only)          1001. Digi Watchport/H
   1002. Temperature@lert               1003. Digi Watchport/T
   1004. iButtonLink T-Sense/T-Probe    1005. **PCsensor USB9097+DS18B20
  ```

- 由上面的信息可知虚拟模式下（Dummy model），功率分析仪和温度传感器：
  - 配置runpower.bat（功率分析仪）：`set DEVICE=0`  
  - 配置runtemp.bat（温度传感器）：`set DEVICE=1000`  
- 实际情况是
  - 配置功率仪DC Tektronix PA1000：`set DEVICE=556`
  - 配置PCsensor USB9097+DS18B20：`set DEVICE=1005`  

#### 2.1.1   runpower.bat or runpower.sh

在linux下更新ptd-linux-x86

```shell
[root@localhost bin]SPEC-updater update ptd-linux-x86 ptd-linux-x86new
```

初始化功率分析仪

对于Windows而言名为`runpower.bat`

- 在`SPECpower/PTDdeamon`目录下，依据系统不同进行各异修改

```shell
# dummy device：虚拟模式，不外接功耗仪器
set DEVICE=0 

# 正常模式：AC PA1000
DEVICE=56
# AC PA1000无法运行在Windows上
# set DEVICE_PORT=COM1              (for Windows) 
```

在Unix而言称为`runpower.sh`

```shell
# dummy device：虚拟模式，不外接功耗仪器
set DEVICE=0 

# 正常模式：AC PA1000
set DEVICE=56
# Unix端的端口
DEVICE_PORT=/dev/usbtmc0         
```
端口选择：usbtmc0

![image-20200925155140768](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200925155140.png)

在目录`/opt/SPECpower/PTDaemon`测试运行一下

```shell
 ./ptd-linux-x86 -p 8888 56 /dev/usbtmc0
 
 # 输出结果
 ...
 Waiting for a connection...
```
#### 2.1.2  runtemp.bat  or runtemp.sh

温度传感器：[USB9097](http://pcsensor.com/1-wire-adapter/usb9097.html) + [DS18B20](http://pcsensor.com/1-wire-series/temperature-probe/dx.html)

在Windows下，名为`runtemp.bat`；在`PTDdeamon`目录下，讲下面几行依据系统不同进行修改

```shell
#  虚拟模式:(dummy temp sensor)
DEVICE=1000 

# 正常模式：USB9097+DS18B20
DEVICE=1005            
DEVICE_PORT=COM3   
```

对于Unix，有一个名为`runtemp.sh`脚本。将温度传感器插入服务器，在`/dev`下，有个接口出现。

![image-20200925155301334](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200925155450.png)

在`PTDdeamon`目录下，讲下面几行依据系统不同进行修改

```shell
# (dummy temp sensor): 虚拟模式
DEVICE=1000 
# 正常模式：USB9097+DS18B20
DEVICE=1005          
DEVICE_PORT=/dev/ttyUSB0
```

#### 2.1.3  SPECpower_ssj.props 与rundirector.bat

要运行`rundirector.bat`

- 在`ssj`目录下，使用前需要配置`SPECpower_ssj.props`

#### 2.1.4 runCCS.bat 与 ccs.props

要运行`runCCS.bat `需要提前配置`ccs.props`

- 在目录`\specpower2008\ccs`下

### 2.2 待测试系统（System Under Test ，SUT）

#### 2.2.1  runssj.bat or runssj.sh

在`ssj`目录下，SPECpower_ssj2008软件使用Java解释器来运行，因此用户必须确保可以通过基准找到Java解释器，在LInux待测试系统和PC端控制系统中编辑`ssj/runssj.bat`或`ssj/runssj.sh`。

```shell
set JAVA=c:\Java\AcmeSuperJava-v5.30\bin\java.exe      (for windows)
JAVA=/usr/local/jdk1.8.0_251/bin/java                  (for unix)
```

如果要使用JVM Director,同时，需要将待测试系统的`runssj.sh`中修改`LOCAL_DIRECTOR`为`FALSE`,并且将`DIRECTOR_HOST`改成控制系统的ip地址。

```shell
set LOCAL_DIRECTOR=FALSE
set DIRECTOR_HOST=192.168.10.101
```

以下的部分并不必要

打开控件属性文件，编辑`SPECpower_ssj_EXPERT.props`,取消 input.director.hostname=localhost 的注释，并且将 hostname 改为待连接的控制器的ip地址(可以在vim中使用 `/`来执行查找)

```shell
input.director.hostname=192.168.10.101 #CCS的ip地址
```

在目录`ssj`下，打开描述性文件`SPECpower_ssj_config.props`，

```shell
config.director.location=hadoop1
```

2.3 Controller System控制系统

在ssj目录下修改`rundirector.bat` (for Windows)

```shell
set JAVA=D:\DevelopmentTools\Java\jdk1.8.0_251\bin\java.exe
```

在ccs目录下，修改runCCS.bat (for Windows)

```shell
set JAVA=D:\DevelopmentTools\Java\jdk1.8.0_251\bin\java.exe
```

在PC端控制器上的`ccs`目录下编辑`runCCS.bat`,更改“set JAVA 行以反映在之前中安装的Java可执行文件的路径。确保将 set SSJHOME =行设置为反映您的SSJ实际安装的路径。

```shell
:: Use a full path name for JAVA if the default JRE is not appropriate
set JAVA=D:\DevelopmentTools\Java\jdk1.8.0_251
set JAVAOPTIONS=
set SSJHOME=C:\Users\Reanon\SPECpower\ssj
```

PC端控制器下的SSJ子目录并编辑rundirector.bat或rundirector.sh文件

```shell
:: Set JAVA to Java.exe path.
set JAVA=D:\DevelopmentTools\Java\jdk1.8.0_251\bin
```

## 三、操作流程

### 具体流程

3.1 调试功耗仪器保证能正确显示服务器电压，电流和功率运行状况

3.2 在PC控制端依次运行以下批处理文件

- runpower.bat    (lspecpower2008\ptd目录下，使用前需要配置它本身)
- runtemp.bat     (\specpower2008\ptd目录下)
- rundirector.bat     (\specpower2008\ssj目录下，使用前需要配置SPECpower_ssj.props)

3.3 在测试服务器端运行以下批处理文件

- runssj.bat(lspecpower2008\ssj目录下，使用前需要配置它本身)
  运行完后过几秒钟可以看到起了几个java的命令行窗口并且和PC端的rundirector.bat有协议握手，表示和服务器连上了。

3.4.在PC控制端运行以下批处理文件完成整个测试

- runCCS.bat(\specpower2008\ccs目录下，使用前需要配置ccs.props)

如果需要结果显示的地方符合实际，需要修改一些SPECpower_ssj_config.props和SPECpower_ssj config _sut.props的值（不修改对结果没影响）

### 测试方法

在linux中查询两端是否在连接

```shell
# tcpdump host [控制端ip] and tcp
tcpdump host 192.168.10.101 and tcp
```

## 四、详细操作

### 4.1 CCS控制端 配置

#### 4.1.1  runpower.bat

**初始化功率分析仪**设置为dummy device 。

- 对于Windows而言名为`runpower.bat`或对于Unix而言称为`runpower.sh`
- 在`SPECpower/PTDdeamon`目录下，依据系统不同进行各异修改
- 根据情况（虚拟模式和实际模式）修改
  - 虚拟模式：`set DEVICE=0`和`set DEVICE_PORT=COM1`

```bash
:: Windows batch file to run ptd in power mode

:: See the Hardware Setup Guide for advanced configurations including GPIB usage

@echo off
echo.

:: Use a full path name for the ptd executable if it is not in the current directory
set PTD=ptd-windows-x86.exe

:: Set NETWORK_PORT if needed.  8888 is the default used by CCS for the power device
set NETWORK_PORT=8888

:: Set DEVICE to the power analyzer device you will use (0=dummy device)
::  use the numeric value found in the help output of the ptd executable
set DEVICE=0

:: Set DEVICE_PORT to the serial port you will connect your power analyzer to
set DEVICE_PORT=COM1

:: Start PTDaemon without logging into logfile
%PTD% -p %NETWORK_PORT% %GPIB_DEVICE% %DEVICE% %DEVICE_PORT%

# 这是其他的配置方式，注释是在pause前面添加::
::  Start PTDaemon with logging of only the measurement data into log-power.csv
::  %PTD% -l log-power.csv -p %NETWORK_PORT% %GPIB_DEVICE% %DEVICE% %DEVICE_PORT%
 
::  Start PTDaemon with extended logging of the measurement data and important events 
::  like range settings, warnings or errors into logext-power.csv
::  %PTD% -l logext-power.csv -e -p %NETWORK_PORT% %GPIB_DEVICE% %DEVICE% %DEVICE_PORT%
```

#### 4.1.2 runtemp.bat  

- 对于Unix，有一个名为`runtemp.sh`脚本
- 在`specpower/PTDdeamon`目录下，讲下面几行依据系统不同进行修改
- 根据情况（虚拟模式和实际模式）修改
  - 虚拟模式：`set DEVICE=1000` 和`set DEVICE_PORT=COM1`

```bash
:: Windows batch file to run ptd in temperature mode

:: See the Hardware Setup Guide for advanced configurations including GPIB usage

@echo off
echo.

:: 
:: NOTE: make sure your sensor is located per Run and Reporting Rules 2.13.3
::  "temperature must be measured no more than 50mm in front of (upwind of)
::     the main airflow inlet of the SUT"
::

echo NOTE: make sure your sensor is located per Run and Reporting Rules 2.13.3
echo "temperature must be measured no more than 50mm in front of (upwind of)
echo  the main airflow inlet of the SUT"
echo.

:: Use a full path name for the ptd executable if it is not in the current directory
set PTD=ptd-windows-x86.exe

:: Set NETWORK_PORT if needed.  8889 is the default used by CCS for the temperature sensor
set NETWORK_PORT=8889

:: Set DEVICE to the sensor device you will use (1000=dummy temp sensor)
::  use the numeric value found in the help output of the ptd executable,设置为虚拟模式.
::温度传感器PCsensor USB9097+DS18B20
::set DEVICE=1000 
set DEVICE=1005

:: Set DEVICE_PORT to the serial port you will connect your sensor to
::set DEVICE_PORT=COM1
set DEVICE_PORT=COM3

:: Start PTDaemon without logging into logfile
%PTD% -t -p %NETWORK_PORT% %DEVICE% %DEVICE_PORT%
```

#### 4.1.3 rundirector.bat    

- 在目录`\specpower2008\ssj`下需要提前配置`rundirector.sh`和`SPECpower_ssj.props`
- 不需要修改

```bash
:: SPECpower_ssj rundirector.bat
::
:: This is an example of what a run script might look like
::
@echo off

:: Number of hosts
set NUM_HOSTS=1

:: Set java options for director
set JAVAOPTIONS_DIRECTOR=-Xms64m -Xmx1024m

:: Properties file to be passed to Director
set PROPFILE=SPECpower_ssj.props

:: Set JAVA to Java.exe path.
set JAVA=java
:: if JAVA not set, let's find it.
if $%JAVA%$ == $$ goto findjava

goto foundjava

:findjava
:: Note, this algorithm finds the last occurance of java.exe in path.
echo Attempting to find java...
for %%p in ( %PATH% ) do if exist %%p\java.exe set JAVA=%%p\java
if $%JAVA%$ == $$ goto nojava
echo Found java: %JAVA%

:foundjava
@echo on
%JAVA% -version
@echo off
goto stage1

:nojava
echo No java?  Please make sure that the path to java is set in your environment!
echo Current PATH: %PATH%
goto egress

:stage1
set SSJJARS=.\ssj.jar;.\check.jar;.\lib\jcommon-1.0.16.jar;.\lib\jfreechart-1.0.13.jar
if "%CLASSPATHPREV%" == $$ set CLASSPATHPREV=%CLASSPATH%
set CLASSPATH=
goto stage2

:stage2
set CLASSPATH=%SSJJARS%;%CLASSPATHPREV%
echo Using CLASSPATH entries:
for %%c in ( %CLASSPATH% ) do echo %%c

:stage3
@echo on
@echo.
@echo Starting Director
%JAVA% %JAVAOPTIONS_DIRECTOR% org.spec.power.ssj.Director -numHosts %NUM_HOSTS% -propfile %PROPFILE%
@echo off

goto egress

:egress

```

#### 4.1.4 SPECpower_ssj.props

- 在目录`\specpower2008\ssj`下需要提前配置`rundirector.bat`和`SPECpower_ssj.props`
- 不需要修改

```bash
#########################################################################
#                                                                       #
#     Control parameters for SPECpower_ssj2008 benchmark                #
#                                                                       #
#########################################################################

#  Each parameter is preceded by an expanatory comments section
#  containing the following information:
#   - a terse description of the parameter
#   - the default value (used if the parameter is commented out)
#   - the range of compliant values
#   - optional additional information on meaning or usage
#   - optional examples of parameter usage.
#
#  This file has 2 sections: changeable parameters and fixed parameters.
#  The fixed parameters exist so that you may run tests any way you want,
#  however in order to have a valid, reportable run of SPECpower_ssj2008,
#  you must reset them to their original values or comment them out.
#
#  Modification of the values of parameters in the fixed parameters
#  section or modification of the values in the changeable parameters
#  section to  values outside the compliant ranges, will result in
#  benchmark runs and results which are not compliant with the benchmark
#  run rules.  Information, data or conclusions produced from runs which
#  are not in compliance with the run rules should not be represented as
#  SPECpower_ssj2008 benchmark results either privately or publicly.  It
#  is a violation of your license agreement to do so.  Please consult the
#  run rules documentation for additional requirements for compliant
#  benchmark runs and publication.

#########################################################################
#                                                                       #
#     Changeable input parameters                                       #
#                                                                       #
#########################################################################

#  The total number of emulated warehouses.
#  Default: Number of logical processors on the SUT (obtained by calling
#   Runtime.getRuntime.availableProcessors()).
#  Compliant: Any change from the default value automatically obtained
#   (by uncommenting this parameter) requires justification, refer to the
#   additional information below and the run rules documentation.
#  Additional: If this property is explicitly set to another value, an
#   explanation must be included in the Notes section.  Refer to the
#   benchmark run rules for details.  In multi-JVM runs, the value of
#   this parameter is divided by the number of JVM instances to determine
#   the number of warehouses used by each individual JVM.
#input.load_level.number_warehouses=8

#  The number of calibration intervals to perform.
#  Default: 3
#  Compliant: any integer >= 3 or <= 10
#  Additional: The final calibration value is calculated as the average
#   of the last 2 of these calibration intervals.  A value of at least 3
#   is recommended because the first interval usually has a lower result
#   than the following intervals.
#input.calibration.interval_count=3

#  The port used for synchronization and data communications from all SSJ
#  instances and the benchmark director.
#  Default: 1500
#  Compliant: any valid and available port value
#input.status.port=1500

#  The name of the descriptive properties file.
#  Default: SPECpower_ssj_config.props
#  Compliant: any valid filename
#  Additional: Descriptive properties define aspects of the system
#   configuration and other conditions that remain constant during the
#   benchmark run.  The common file name is "SPECpower_ssj_config.props".
#   On systems where the file separator is "\", use "\\" as the file
#   separator here (refer to the third example).
#  Examples:
#   input.include_file=SPECpower_ssj_config.props
#   input.include_file=/path/to/SPECpower_ssj_config.props
#   input.include_file=c:\\path\\to\\SPECpower_ssj_config.props
#input.include_file=SPECpower_ssj_config.props

#  The directory in which output files are stored.
#  Default: results
#  Compliant: any value
#  Additional: On systems where the file separator is "\", use "\\" as
#   the file separator here (refer to the third example).
#  Examples:
#   input.output_directory=results
#   input.output_directory=/path/to/results
#   input.output_directory=c:\\path\\to\\results
#input.output_directory=results

#########################################################################
#                                                                       #
#     Fixed input parameters                                            #
#                                                                       #
#     Changes to these values will result in a non-compliant run.       #
#                                                                       #
#########################################################################

#  The workload name.
#  Default: null (note this parameter is uncommented by default)
#  Compliant: SPECpower_ssj
#  Additional: Reserved for future work.  Changing the parameter value or
#   commenting it out will result in benchmark failure to execute.
input.suite=SPECpower_ssj


```

### 4.2  测试服务器端 配置

测试时需要将服务器的防火墙关闭，否则会遇到程序僵死的情况。

#### 4.2.0 切换linux驱动到acpi-cpufreq

安装cpufrequtils

```shell
yum install cpufrequtils
```

要想实现cpu频率的动态调节，需要服务器支持`userspace`模式，一般英特尔。可以使用下面的语句查看当前的cpu支持的模式

```shell
cpupower -c all frequency-info
```

结果为

```shell
analyzing CPU 0:
  driver: intel_pstate #这个intel_pstate就是intel的睿频，只支持performance和powersave模式
  ...
```

如果要将cpu切换到`userspace`模式下，需要将驱动改回`acpi-cpufreq`，这里查了很多资料，发现关于Centos怎么设置为acpi-cpufreq模式的很少。后来试着在`/etc/default/grub`的`GRUB_CMDLINE_LINUX=... `后添加`intel_pstate=disable`

```shell
1.关闭睿频
echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo

(base) [root@bogon ~]# vim /etc/default/grub
```

```shell
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
# 添加 intel_pstate=disable到 GRUB_CMDLINE_LINUX的末尾
GRUB_CMDLINE_LINUX="crashkernel=auto spectre_v2=retpoline rd.lvm.lv=centos/root rd.lvm.lv=centos/swap nomodeset rhgb quiet intel_pstate=disable"
GRUB_DISABLE_RECOVERY="true"
```

加载模块`acpi-cpufreq`

```shell
modprobe acpi-cpufreq
```

再使用grub2-mkconfig工具刷新grub。

```shell
grub2-mkconfig -o /boot/grub2/grub.cfg
```

接下来需要重启一次

```shell
reboot
```

然后查看当前的驱动模式，发现驱动已经切换到了`acpi-cpufreq`。于是能够选择的模式变成了五种，而且可以可选择的频率也出现了。

```shell
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_driver

# 这里是结果
acpi-cpufreq
acpi-cpufreq
acpi-cpufreq
acpi-cpufreq
```

查看cpu的个数以及核数

```shell
# 查询物理CPU个数：
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

# 查询物理核数：
cat /proc/cpuinfo| grep "cpu cores"| uniq

# 查询逻辑CPU总数：
cat /proc/cpuinfo| grep "processor"| wc -l

# CPU型号的查询方式。
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c
```

查询可得实验服务器为一个cpu带4核心的配置

![image-20200831110439139](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200922084632.png)

查看cpu频率（全部）

```shell
# 查看cpu频率（全部）
watch -n 0 "cat /proc/cpuinfo | grep -i mhz"
cat /proc/cpuinfo | grep -i mhz
```

查看当前的调节器

```shell
# 查看当前的调节器
(base) [root@bogon ~]# cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor  
userspace
userspace
userspace
userspace
```

设置全部cpu频率

```shell
# 设置全部cpu频率，当设置为一个数时，会自动靠近离这个值最近的`available frequency steps`
(base) [root@bogon ~]# cat /proc/cpuinfo | grep -i mhz
cpu MHz		: 2100.000
cpu MHz		: 2100.000
cpu MHz		: 2100.000
cpu MHz		: 2100.000
```

cpupower命令设置单个cpu的频率

```shell
# 通过cpupower命令设置单个cpu的频率
(base) [root@bogon ~]# cpupower --cpu 0 frequency-set --freq 1GHz
Setting cpu: 0
(base) [root@bogon ~]# cat /proc/cpuinfo | grep -i mhz
cpu MHz		: 1000.000
cpu MHz		: 2100.000
cpu MHz		: 2100.000
cpu MHz		: 2100.000
```

取得scaling_available_frequencies 的各个值

```shell
# 取得scaling_available_frequencies 的各个值
(base) [root@bogon cpufreq]# cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
3401000 3400000  3200000 3000000 2800000 2700000 2500000 2300000 2100000 1900000 1700000 1500000 1400000 1200000 1000000 800000 
```

这里发现可以通过`cpupower --cpu 0 frequency-set --freq 1000000KHZ`来设置Centos7的频率

```shell
(base) [root@bogon cpufreq]# cpupower --cpu 0 frequency-set --freq 1000000KHZ
Setting cpu: 0
(base) [root@bogon cpufreq]# cat /proc/cpuinfo | grep -i mhz
cpu MHz		: 1000.000
cpu MHz		: 2100.000
cpu MHz		: 2100.000
cpu MHz		: 2100.000
```

#### 4.2.1 runssj.sh

- 在目录`/SPECpower_ssj2008/ssj`下，需要配置远程控制服务端
- `DIRECTOR_HOST=（控制端端口号）`

```shell
#!/bin/sh
## This is an example of what a run script might look like
##

JVMS=1

## Set to TRUE if jvm Director is on this host，设置为FALSE的话就要填入远程的控制端了
LOCAL_DIRECTOR=FALSE
DIRECTOR_HOST=192.168.10.101

## The SETID is used to identify the descriptive configuration properties
## that will be used for the system under test.  For example, with a SETID
## of "sut", the descriptive configuration properties will be read from the
## file SPECpower_ssj_config_sut.props from the Director system.
SETID=sut

DIRECTOR_PROPFILE=SPECpower_ssj.props

## Benchmark run rules require a list of active OS services be retained for publishable runs.
## For Solaris, this can be accomplished by uncommenting the following line.
## svcs -a > services.txt

# 添加以下信息
# 1、打印程序结束
echo finish
# 2、睡眠60秒
sleep 60
# 3、执行结束自动关闭bash终端
kill -1 `ps -o ppid -p $$ | tail -1`
```

#### 4.2.2 runCCS.bat

- `specpower2008\ccs`目录下
- 使用前需要配置`ccs.props`
- 几乎不需要修改

```shell
#!/bin/sh
#

# set JAVA to java executable path
JAVA="java"

# Set JAVAOPTIONS to override any JVM settings when running CCS
JAVAOPTIONS=

# Set SSJHOME to the directory containing ssj.jar
SSJHOME="../ssj"

CP="./ccs.jar:./check.jar:$SSJHOME/ssj.jar:$SSJHOME/lib/jfreechart-1.0.13.jar:$SSJHOME/lib/jcommon-1.0.16.jar"

$JAVA -classpath $CP $JAVAOPTIONS org.spec.power.ccs.SpecPowerCCS ccs.props
```

#### 4.2.3 ccs.props

- `specpower2008\ccs`目录下
- 几乎不需要修改

```shell
ccs.ptd = pwr1, temp1
#ccs.vam = vam1

#####################################################
##
##  Detail Section-topology of the systems and software
##
#####################################################

#
#   Workload Data Source  #################################
#
#   Configure the connection to SSJ Director.
#   If the director is run on a system other than the CCS
#   system, replace "localhost" with the IP address of the 
#   "director" system.  If the SSJ director is started with
#   a non-standard port, change the port number here to match.
#

ccs.wkld.ssj_dir.type = SSJ
ccs.wkld.ssj_dir.IP = localhost
ccs.wkld.ssj_dir.Port = 8886

#
#   Power Analyze 1 Data Source  ########################
#
#  If the PTDaemon is run on a system other than the CCS
#    system, replace "localhost" with the name or IP address
#    of that system.
#  If PTDaemon is started with a TCP/IP port other than the 
#    default, change the port number below to match the 
#    port number in the PTDaemon script file.
#

ccs.ptd.pwr1.type = PowerAnalyzer
ccs.ptd.pwr1.IP = localhost
ccs.ptd.pwr1.Port = 8888

#
# Power Analyzer Range Settings ##########################
#
# Select Power analyzers have multiple ranges that can be
#   set by the front panel or programmatically.

# Ranges can be set for current (amps) and voltage, 
#  and can be set or changed for each benchmark load level. 
#  
# Range settings are sent to the power analyzer, 
#   only if the device supports programmatic setting.
#
# A range may be specified for each load level.

# The range value should be the maximum of 
#   the power analyzer's range setting.

# If a range setting is left blank, 
#   or no setting property is 
#   present for that meter (or commented out),
#   then existing meter settings will be used.

# Some analyzers must be set up on the front panel.
#   If range settings are entered at the analyzer, 
#   those range(s) must be recorded in the 
#   configuration section below.

# For compliant benchmark runs, and by default, 
#   the SPECpower_ssj2008 benchmark generates 
#   14 load levels; 
#     3 calibration, and 11 graduated levels.

# Ranges for the levels are set by a comma separated
#   list that may contain one or more range values. 
# The position of a range in the string is a 1:1
#   match to the load level. 
#    Spaces are ignored. 
# Comma separators are required except after the
#   last value.

# Example 1: Auto for all levels
#    ptd.pwr1.current_range_settings = auto

# Example 2: 4 amps for calibration and 100%, 
#   then 2 for all other load levels
#    ptd.pwr1.current_range_settings = 4, 4, 4, 4, 2

# Example 3; 5 amps for levels down to 80%, 
#   then 2 amps for levels 70% and below:
#    ptd.pwr1.current_range_settings= 5, 5, 5, 5, 5, 5, 2

# The load levels are in this order: 
#  cal1, cal2 cal3, 100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%, idle 

ccs.ptd.pwr1.current_range_settings=auto

#  Given voltage is expected to be constant for a given
#    run of the benchmark, voltage_range need only be set
#    for the first level; for example: 
#  ccs.ptd.pwr1.voltage_range_settings = 120

ccs.ptd.pwr1.voltage_range_settings=auto

#
# Temperature Sensor 1 connection ########################
#
#  If the PTDaemon is run on a system other than the CCS
#    system, replace "localhost" with the name or IP address
#    of the system running the PTDaemon.
#  If PTDaemon is started with a TCP/IP port other than the 
#    default, change the port number below to match the 
#    port number in the PTDaemon script file.

ccs.ptd.temp1.type = TempSensor
ccs.ptd.temp1.IP = localhost
ccs.ptd.temp1.Port = 8889

#
#   Power Analyzer 2 Data Source  ########################
#
#  See the comments for power analyzer 1 above.  Note that
#   for these entries to be used, "pwr2" must be added to
#   the ccs.ptd data sources above.
#

#ccs.ptd.pwr2.type = PowerAnalyzer
#ccs.ptd.pwr2.IP = localhost
#ccs.ptd.pwr2.Port = 8890

#
#   VAM Connection Configuration #######################
#
# If VAM is run on a system other than the CCS
#   system, replace "localhost" with the host name or
#   or IP address of that system.

# The port number below is the default for one of three
#   potential instances of CCS from which VAM can display data. 
#  
# If this instance of CCS is the second or third for VAM,
#   the port number below must match that of the port number
#   in the vam.props file.  
#

ccs.vam.vam1.type = VAM
ccs.vam.vam1.IP = localhost
ccs.vam.vam1.Port = 8905

# 
#  To enable synchronization of multiple data sources read by
#    VAM, the "syncStart" parameter must be set to True
#    in the ccs.props file for each instance of CCS, 
#    and in the vam.props file.  
#  SyncStart causes CCS and therefore all Directors to
#    wait until all are ready.  
#

ccs.vam.syncStart = false

#####################################################
##
##  CCS Configuration Info Sections
##
#####################################################

#
#  The following properties will be used by the 'reporter'.
#
#  Change as needed to reflect the details of the 
#   equipment in your setup.
#

#####################################################
##
##  CCS system (platform) hardware and software info
##
#####################################################

#
#   Company which sells/manufactures the hardware.
#

ccs.config.hw.vendor=IQ2 Corporation

#
#   Model name of CCS platform / system
#

ccs.config.hw.model=Meridian 38

#
#   Make and model of the processor(s) in the CCS system.
#

ccs.config.hw.cpu=Saturn ULP

#
#   Basic info on the processor, e.g. single/dual core, clock speed,
#   cache sizes.
#

ccs.config.hw.cpu.characteristics=3.2 GHz, dual core, 2M L2 cache, 4M L3 cache

#
#   The amount of main memory in the CCS system in GigaBytes.
#

ccs.config.hw.memory.gb=1.5

#
#   CCS host Operating System
#

ccs.config.sw.os=SPEC Open Doors 2006 F500

#
#   JVM vendor name and version used on CCS system.
#

ccs.config.sw.jvm.vendor=IQ2 Corporation
ccs.config.sw.jvm.version=IQ2 Java VM v1.0

#####################################################
##
##  Basic info on Power Analyzer
##
#####################################################

#
#   Power analyzer manufacturer.
#

ptd.pwr1.config.analyzer.vendor=Energy Minder, Inc.

#
#   Model name of the power analyzer - usually on front panel.
#

ptd.pwr1.config.analyzer.model=EM1000+ USB

#
#   Serial number of the power analyzer.
#

ptd.pwr1.config.analyzer.serial=ser001122

#
#   Data connection from power analzer to the
#   host system, e.g. USB, RS-232, GPIB, LAN.
#   If a USB to serial converter is used, the brand 
#   and model should be entered in the Notes. 
#

ptd.pwr1.config.analyzer.connectivity=USB2

#
#   Power Analyzer Calibration and Certification
#
#   Name of the national metrology institute or organization
#   which specifies calibration specs and standards
#

ptd.pwr1.config.calibration.institute=NIST

#
#   Name of the organization that performed the power analyzer calibration.  
#   Could be the analyzer manufacturer, a third party company, or an 
#   organization within your own company. 
#

ptd.pwr1.config.calibration.accredited_by=IQ2 Calibration Laboratory

#
#   The number which uniquely identifies this device calibration event.
#   May appear on the certification certificate or on a sticker applied
#   to the power analyzer.  The format of this number is specified by
#   the calibration institute.
#

ptd.pwr1.config.calibration.label=N-32768

#
#   Date of calibration, from the calibration paperwork or sticker.
#   Day-Month-Year
#

ptd.pwr1.config.calibration.date=1-Jan-2007

#
#   Manufacturer and model number of the computer system to which the power
#   analyzer data cable is connected, and the operating system of that
#   computer.  This is the system specified by ccs.ptd.pwr1.IP above.  It
#   may be the same as the CCS system.
#

ptd.pwr1.config.ptd.system=same as CCS
ptd.pwr1.config.ptd.os=same as CCS

#
#   input_connection: input used to connect the load, if several options are 
#     available, or "Default" if not.
#   current_range: value of power analyzer current range configuration if 
#     PTD cannot automatically determine the range. Or "Auto" if none
#   voltage_range: value of power analyzer voltage range configuration if 
#     PTD cannot automatically determin ther range. Or "Auto" if none
#

ptd.pwr1.config.analyzer.input_connection = Default
ptd.pwr1.config.analyzer.current_range = Auto
ptd.pwr1.config.analyzer.voltage_range = Auto

#
# The 'analyzer.setup_description' property describes
# which device or devices are measured for this instance
# of a power analyzer and the PTDaemon. 
#
# This should be a textual description
# of the device or devices measured. 
# Example: 
# analyzer.setup_description= SUT Power Supplies 1 and 2
#
# The default is a null string (blank)
#

ptd.pwr1.config.analyzer.setup_description=

#####################################################
##
##  Basic info on Temperature Sensor
##
#####################################################

#
#   Temperature sensor manufacturer.
#

ptd.temp1.config.sensor.vendor=EnviroBits, Inc.

#
#   Temperature sensor model name.
#

ptd.temp1.config.sensor.model=Tsense USB-2

#
#   Name of and version number of temperature sensor driver.
#

ptd.temp1.config.sensor.driver=1.2.3.4

#
#   Data connection from temperature sensor to the
#   host system, e.g. USB, RS-232, GPIB, LAN.
#   If a USB to serial converter is used, the brand 
#   and model should be entered in the Notes. 
#

ptd.temp1.config.sensor.connectivity=USB

#
#   Manufacturer and model number of the computer system to which the 
#   temperature sensor data cable is connected, and the operating system 
#   of that computer.  This is the system specified by ccs.ptd.temp1.IP 
#   above.  It may be the same as the CCS system.
#

ptd.temp1.config.ptd.system=same as CCS
ptd.temp1.config.ptd.os=same as CCS

#
#
# The 'sensor.setup_description' property describes
# which device or devices are measured for this instance
# of a temperature sensor and the PTDaemon. 
#
# This should be a textual description
# of the device or devices measured and the 
# approximate location of the temperature sensor. 
# Example: 
# sensor.setup_description= 5 mm in front of SUT main intake 
#
# The default is a null string (blank)
#

ptd.temp1.config.sensor.setup_description=

#
#####################################################
##
##  End of CCS properties
##
#####################################################
```

如果需要结果显示的地方符合实际，需要修改一些SPECpower_ssj_config.props和SPECpower_ssj config _sut.props的值（不修改对结果没影响）

## 五、执行过程日志

### 5.1 PC端

#### 5.1.1 运行runpower.bat

- `\SPECpower\PTDaemon`目录下，点击运行runpower.bat

执行的过程，等待连接

```shell
 ****************************************************************************
                SPECpower Power/Temperature Daemon version 1.4.2
                     Licensed Materials - Property of SPEC
     Copyright 2006-2012 Standard Performance Evaluation Corporation (SPEC)
                              All Rights Reserved.
                 Copyright 2006 Dell Inc.  All Rights Reserved.
  For use with benchmark products from SPEC and authorized organizations only.
  ****************************************************************************
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!  WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Warning!  Your SPEC PTDaemon version is more than 6 months old!
                Please check www.spec.org for possible updates.
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!  WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Selected power meter 'Dummy (testing only)' from dummy.cpp
Calculating ptd CRC...0xbc965ca0, 1040384
08-14-2020 12:27:56.728: Attempting to connect to measurement device type 0...
08-14-2020 12:27:56.729: Dummy identifies: SPECpower's Dummy Analyzer
08-14-2020 12:27:56.729: Uncertainty checking for Dummy is activated
08-14-2020 12:27:56.729: Connected to Dummy successfully
08-14-2020 12:27:56.729: Establishing the listener on port 8888...
08-14-2020 12:27:56.741: Waiting for a connection...
```

#### 5.1.2 运行runtemp.bat   

- `\SPECpower\PTDaemon`目录下点击runtemp.bat  
- 执行日志如下

```shell
NOTE: make sure your sensor is located per Run and Reporting Rules 2.13.3
"temperature must be measured no more than 50mm in front of (upwind of)
 the main airflow inlet of the SUT"

  ****************************************************************************
                      ***********************************
                               SPEC PTDaemon Tool
                        Version 1.9.1-a2d19f26-20190717
                      ***********************************
                     Licensed Materials - Property of SPEC
     Copyright 2006-2019 Standard Performance Evaluation Corporation (SPEC)
                              All Rights Reserved.
  For use with benchmark products from SPEC and authorized organizations only.
  ****************************************************************************


Selected temperature meter 'PCsensor USB9097+DS18B20' from ibuttonlink.cpp
Calculated PTD CRC: 0xa2d19f26, 2017792
09-23-2020 14:36:59.512: Attempting to connect to measurement device type 1005...
09-23-2020 14:36:59.523: Maxim IBFS32.DLL found.
09-23-2020 14:37:00.390: Connected to PCsensor USB9097+DS18B20 successfully
09-23-2020 14:37:00.391: Establishing the listener on port 8889...
09-23-2020 14:37:00.395: Waiting for a connection...
09-23-2020 14:40:10.502: Accepted connection from 127.0.0.1:2419
09-23-2020 14:40:11.513: Response to client sent: PCsensor USB9097+DS18B20,5000,1,0,0,0,0,0,1,version=1.9.1-a2d19f26-20190717,OS=Windows 8 / Server 2012,mode=temperature,0,0,1,0,0,no_cal_date,na
09-23-2020 14:40:22.721: Response to client sent: Starting untimed measurement, maximum 500000 samples at 5000ms with 0 rampup samples
09-23-2020 14:40:22.793: Response to client sent: No data
09-23-2020 14:40:23.800: Response to client sent: No data
09-23-2020 14:40:23.964,Temp,29.687500,Humidity,0.000000,Mark,notset
09-23-2020 14:40:24.809: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:25.817: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:26.824: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:27.731: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:28.739: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:28.965,Temp,29.687500,Humidity,0.000000,Mark,notset
09-23-2020 14:40:29.748: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:32.569: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:33.580: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:33.964,Temp,29.687500,Humidity,0.000000,Mark,notset
09-23-2020 14:40:34.59909-23-2020 14:40:38.963,Temp,29.687500,Humidity,0.000000,Mark,notset
: Response to client sent: Temperature,29.687500,Humidity,0.000000
09-23-2020 14:40:44.382: WARNING: Missed 1 samples
09-23-2020 14:40:44.383,Temp,-2.000000,Humidity,-2.000000,Mark,notset
09-23-2020 14:40:44.483: Response to client sent: Temperature,-2.000000,Humidity,-2.000000
...
```

#### 5.1.3 运行rundirector.bat   

- `\SPECpower\ssj`目录下点击rundirector.bat   
- 等待端口的输入

```shell
C:\SPECpower\ssj>java -version
java version "1.8.0_231"
Java(TM) SE Runtime Environment (build 1.8.0_231-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.231-b11, mixed mode)
Using CLASSPATH entries:
.\ssj.jar
.\check.jar
.\lib\jcommon-1.0.16.jar
.\lib\jfreechart-1.0.13.jar

Starting Director

C:\SPECpower\ssj>java -Xms64m -Xmx1024m org.spec.power.ssj.Director -numHosts 1 -propfile SPECpower_ssj.props
Starting Director for SSJ 1.2.10 (May 9, 2012)

Command-line properties are COMPLIANT

Opened results\director\SPECpower_ssj.0039\ssj.0039.director.results
Opened results\director\SPECpower_ssj.0039\ssj.0039.director.raw

Licensed Materials - Property of SPEC
SPECpower_ssj2008
Copyright (c) 2005-2012 Standard Performance Evaluation Corporation (SPEC),All rights reserved,

Waiting for jvm 1 on port 1500
Host JVM id: localhost.localdomain.001
Accepted synchronization client for jvm "localhost.localdomain.001" at /192.168.10.100:52352

Searching for extraneous jvm connections for 10 seconds...
The number of jvms started appears to match the number specified.


Uncertainty of clock offsets is ~ 0ms
Waiting for jvm "localhost.localdomain.001" data collector on port 1500
Accepted data collector client for "localhost.localdomain.001" at /192.168.10.100:52368
Director ready for CCS connection
jar validity is true
Directing 1 jvm instances

Preparing to synchronize for 3 calibration measurements...
interval 1 : Reading READY state from the jvm instances
interval 1 : Received READY from all, now sending START
interval 1 : Calibration 1 run in progress...
interval 1 : Calibration 1 run completed.
interval 2 : Reading READY state from the jvm instances
interval 2 : Received READY from all, now sending START
interval 2 : Calibration 2 run in progress...
interval 2 : Calibration 2 run completed.
interval 3 : Reading READY state from the jvm instances
interval 3 : Received READY from all, now sending START
interval 3 : Calibration 3 run in progress...
interval 3 : Calibration 3 run completed.
# 开始正式运行
Preparing to synchronize for 10 load level measurements...
interval 1 : Reading READY state from the jvm instances
interval 1 : Received READY from all, now sending START
interval 1 : 100% run in progress...
interval 1 : 100% run completed.
interval 2 : Reading READY state from the jvm instances
interval 2 : Received READY from all, now sending START
interval 2 : 90% run in progress...
interval 2 : 90% run completed.
interval 3 : Reading READY state from the jvm instances
interval 3 : Received READY from all, now sending START
...
interval 10 : Received READY from all, now sending START
interval 10 : 10% run in progress...
interval 10 : 10% run completed.

# 这段会运行很长时间
Preparing to synchronize for 1 active idle post-run measurements...
interval 1 : Reading READY state from the jvm instances
interval 1 : Received READY from all, now sending START
interval 1 : Active Idle run in progress...
interval 1 : Active Idle run completed.

# 准备总结成报告
Reading FINISHED state from the jvm instances
Received FINISHED from all jvm instances, now summarize the reports...
```

 (\specpower2008\ssj目录下，使用前需要配置SPECpower_ssj.props)

### 5.2 测试服务器端运行

#### 5.2.1 runssj.sh

- `/SPECpower_ssj2008/ssj`目录下,使用前需要配置它本身
- 执行runssj.sh：`[root@hadoop1 ssj]# ./runssj.sh`

- rundirector.bat上的日志更新：运行完后过几秒钟可以看到起了几个java的命令行窗口并且和PC端的rundirector.bat有协议握手，表示和服务器连上了。

```shell
# 这是运行在PC端的rundirector.bat的日志更新
Uncertainty of clock offsets is ~ 0ms
Waiting for jvm "hadoop1.001" data collector on port 1500
Accepted data collector client for "hadoop1.001" at /192.168.182.130:54180
Director ready for CCS connection
```

在服务端的runssj.sh运行结果

```shell
[root@hadoop1 ssj]# ./runssj.sh
2020年 08月 17日 星期一 00:09:42 CST
java version "1.8.0_251"
Java(TM) SE Runtime Environment (build 1.8.0_251-b08)
Java HotSpot(TM) 64-Bit Server VM (build 25.251-b08, mixed mode)
Starting instance 1
# 这里就是收到FINISHED state之后会刷出的状态
JFreeChart Copyright (C) 2000-2009, Object Refinery Limited and Contributors. (jFreeChart licences available in the redistributable_sources directory)

2020年 08月 17日 星期一 01:23:05 CST
```



### 5.3 在PC控制端运行完成整个测试

#### 5.3.1 运行runCCS.bat

- `\SPECpower\ccs`目录下，使用前需要配置ccs.props
- 点击runCCS.bat，发现runpower.bat 和 runtemp.bat 上更新数据，即算是运行成功

```shell
C:\SPECpower\ccs>set JAVA=java

C:\SPECpower\ccs>set JAVAOPTIONS=

C:\SPECpower\ccs>set SSJHOME=..\ssj

C:\SPECpower\ccs>set CP=.\ccs.jar;.\check.jar;..\ssj\ssj.jar;..\ssj\lib\jfreechart-1.0.13.jar;..\ssj\lib\jcommon-1.0.16.jar

C:\SPECpower\ccs>java -classpath .\ccs.jar;.\check.jar;..\ssj\ssj.jar;..\ssj\lib\jfreechart-1.0.13.jar;..\ssj\lib\jcommon-1.0.16.jar  org.spec.power.ccs.SpecPowerCCS ccs.props
***********************************************************************
                    ccs.jar version 1.2.6    May 09, 2012
                 Licensed Materials - Property of SPEC
Copyright 2006-2012 Standard Performance Evaluation Corporation (SPEC)
                          All Rights Reserved
***********************************************************************
Waiting for wkld.ssj_dir ptd.pwr1 ptd.temp1 to connect... [0] seconds
=====> start client run for ptd.temp1<=====

=====> start client run for ptd.pwr1<=====

=====> start client run for wkld.ssj_dir<=====

=====> Connected <=====
*** Warning: ptd.pwr1(Dummy-no_cal_date-SPECpower's Dummy Analyzer v1.0) is not certified for compliant SPECPower_ssj2008 results
*** Warning: ptd.temp1(DummyTemp-no_cal_date-na) is not certified for compliant SPECPower_ssj2008 results
=====> Ready for testing <=====
start: wkld.ssj_dir
start: ptd.pwr1
start: ptd.temp1
=====> Start testing <=====
=====> wkld.ssj_dir benchmark state changed to _001_cal_ru_ <=====
=====> wkld.ssj_dir benchmark state changed to _001_cal_rc_ <=====
=====> wkld.ssj_dir benchmark state changed to _001_cal_rd_ <=====
=====> wkld.ssj_dir benchmark state changed to _inter_ <=====
=====> wkld.ssj_dir benchmark state changed to _002_cal_ru_ <=====
=====> wkld.ssj_dir benchmark state changed to _002_cal_rc_ <=====
=====> wkld.ssj_dir benchmark state changed to _002_cal_rd_ <=====
=====> wkld.ssj_dir benchmark state changed to _inter_ <=====
=====> wkld.ssj_dir benchmark state changed to _003_cal_ru_ <=====
=====> wkld.ssj_dir benchmark state changed to _003_cal_rc_ <=====
=====> wkld.ssj_dir benchmark state changed to _003_cal_rd_ <=====
=====> wkld.ssj_dir benchmark state changed to _inter_ <=====
=====> wkld.ssj_dir benchmark state changed to _001_lvl_ru_ <=====
=====> wkld.ssj_dir benchmark state changed to _001_lvl_rc_ <=====
=====> wkld.ssj_dir benchmark state changed to _001_lvl_rd_ <=====
lvl target = 101117 (100.00%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _inter_ <=====
lvl target = 101117, lvl actual = 93266 (92.24%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _002_lvl_ru_ <=====
=====> wkld.ssj_dir benchmark state changed to _002_lvl_rc_ <=====
=====> wkld.ssj_dir benchmark state changed to _002_lvl_rd_ <=====
lvl target = 91005 (90.00%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _inter_ <=====
lvl target = 91005, lvl actual = 78933 (86.73%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _003_lvl_ru_ <=====
=====> wkld.ssj_dir benchmark state changed to _003_lvl_rc_ <=====
=====> wkld.ssj_dir benchmark state changed to _003_lvl_rd_ <=====
lvl target = 80894 (80.00%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _inter_ <=====
lvl target = 80894, lvl actual = 80504 (99.52%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _004_lvl_ru_ <=====
=====> wkld.ssj_dir benchmark state changed to _004_lvl_rc_ <=====
=====> wkld.ssj_dir benchmark state changed to _004_lvl_rd_ <=====
lvl target = 70782 (70.00%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _inter_ <=====
lvl target = 70782, lvl actual = 70462 (99.55%), cal target = 101117
=====> wkld.ssj_dir benchmark state changed to _005_lvl_ru_ <=====
```

### 5.4  可视化数据

- 在目录`\SPECpower\vam`下，直接执行runVAM.bat

### 5.5 执行示意图

#### 5.5.1 窗口示意图

在PC端上runpower.bat 和 runtemp.bat 上不停地更新数据

- runtemp.bat会返回虚拟的温度数据：`Response to client sent: Temperature,21.222000,Humidity,55.555500`
- runpower.bat会返回虚拟的功耗数据：`08-14-2020 12:52:54.153,Watts,23.310000,Volts,120.000000,Amps,0.194250,PF,1.000000,Mark,_002_cal_rc_`
- rundirector.bat记录执行状态，如校准（calibration）、准备等。

![image-20200814125139488](https://gitee.com/Reanon/upload-markdown-img/raw/master/img/20200829190743.png)

#### 5.5.2 数据可视化

- 在目录`\SPECpower\vam`下，运行`runVAM.bat`

