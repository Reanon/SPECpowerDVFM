# 基于SPECpower_ssj2008的动态电压频率调节

## 一、简单介绍

### 实验目的

本项目是测试服务器在不同工作频率下的功耗情况，也即动态电压频率调节（Dynamic Voltage and Frequency modulation，DVFM）。

The Standard Performance Evaluation Corporation ([SPEC](https://www.spec.org/))出品的SPECpower_ssj2008软件，SPECpower_ssj2008是用于评测系统级别服务器的与运算性能相关的功耗的基准测试工具。

### 实验设备

1. 功耗仪：[PA1000](http://www.tek.com/power-analyzer/pa1000)
2. 温度传感器：[USB9097](http://pcsensor.com/1-wire-adapter/usb9097.html) + [DS18B20](http://pcsensor.com/1-wire-series/temperature-probe/dx.html)
3. 待测服务器：[戴尔PowerEdge R740 机架式服务器](https://www.dell.com/zh-cn/work/shop/povw/poweredge-r740)
4. 控制端：联想普通主机

### 实验方案

通过逐步调节服务器的CPU频率等级，运行SPECpower测试在当前频率下服务器的功耗情况，CPU的频率由高到底，直到将服务器可用的所有频率等级都进行测试。例如，某服务器有4个CPU（CPU0，CPU1，CPU2，CPU3），每个CPU都相同，单个CPU可调节频率有10级（这里假设10级为该CPU最高频率的等级）。那么就首先将CPU0的工作频率从10级逐级下调到1级，然后关闭CPU0，对CPU1、CPU2也是同理，直到调整到CPU3的第1级。

每调整一次频率，都会运行一次SPECpower_ssj2008程序测量当前频率下的功耗情况，并得出一份功耗分析的报告。

最后通过分析这些不同频率等级下的功耗情况，确定出服务器功耗和CPU频率之间的关系，以便为后期的服务器集群任务调度分析奠定基础。

## 二、目录结构

### docs

该文件夹下提供了一些说明文档：

1、SPECpower_ssj2008使用指南

该软件在购买之后，虽然提供了较为详实的官方参考文档[SPECpower_ssj2008-Quick_Start_Guide.pdf](https://github.com/SEU-SSL/SPECSokcet/blob/main/Documentation/SPECpower_ssj2008-Quick_Start_Guide.pdf)和[SPECpower_ssj2008-User_Guide.pdf](https://github.com/SEU-SSL/SPECSokcet/blob/main/Documentation/SPECpower_ssj2008-User_Guide.pdf)。但是在实际测试过程中还是遇到了不少的问题，这里将自己的操作流程十分详细地写在中SPECpower操作指南中，希望之后向要进行这方面测试的同学可以少走一些弯路，获得一些收获。

2、SPEC的官方指导文档

3、功耗仪PA1000的中文操作手册：[PA1000-User-Manual-ZH.pdf](https://github.com/SEU-SSL/SPECSokcet/blob/main/Documentation/PA1000-User-Manual-ZH.pdf)

4、设置戴尔工作站BIOS的操作手册：[Setting_BIOSin14G-Serv(16Apr2018).pdf](https://github.com/SEU-SSL/SPECSokcet/blob/main/Documentation/Setting_BIOSin14G-Serv(16Apr2018).pdf)

### SPECSokcet

该目录下存放Python编写的控制端（CCS）与测试端（SUT）以网络通信方式来完成整个测试流程的代码。

1. clinetSocket：包含着tcp、udp网络通信客户端（也即CCS端）的代码
2. severSocket：包含着tcp、udp网络通信服务端（也即SUT端）的代码
3. test：程序调试过程中的测试程序，无需在意。
4. utils：编写的一些工具方法

在执行SPECSokcet程序时，需要现在服务端（SUT）开启运行`sever_tcp.py`，再在客户端（CCS）运行`main.py`。

注意：能够运行==成功的前提是正确配置好了SPECpower_2008==。

### SPECAnalysis

存放分析Result文件下的数据的代码。

### Results

用以存放服务器在不同频率下的功耗SPECpower_ssj2008输出结果。

