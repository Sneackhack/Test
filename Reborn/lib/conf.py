#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""用于读取本项目rb.conf配置文件"""

from platform import system, release, node
from configparser import ConfigParser

conf = ConfigParser()
conf.read("rb.conf", encoding="utf-8")

username = conf.get("General", "username")  # 用户名, 用于区分设备, 默认是详细系统名
path = conf.get("General", "download_path")  # 下载目录
recv_size = conf.getint("Advanced", "one-time_recv_size")  # 一次性接收数据最大大小
recv_ip = conf.get("Advanced", "recv_ip")  # 接收文件时使用的局域网IP地址, 不填写则自动获取
recv_port = conf.getint("Advanced", "recv_port")
send_port = conf.getint("Advanced", "send_port")

if not username:
    username = system() + release() + node()  # 将用户名设置为系统名 + 计算机名

if path[-1] == "/" or path[-1] == "\\":
    path = path.rstrip("\\").rstrip("/")
