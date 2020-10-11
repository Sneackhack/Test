#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""本项目网络相关的函数"""

import socket
from os import rename
from time import sleep

from .conf import recv_size, path, username

host_list = []  # 搜索到的设备列表


def _get_host_ip():
    """通过谷歌DNS获取自身IP地址, 如果失败则用socket.gethostbyname函数获取"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        addr = s.getsockname()[0]
    except:
        addr = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return addr


def send(file_name, addr, port=61008):
    """发送文件, 返回发送情况"""
    conn = socket.socket()
    file = open(file_name, "rb")
    data = bytes

    try:
        conn.connect((addr, port))
        ck = conn.recv(1024).decode()
        if ck == "1":
            return "The other side is busy"
        elif ck != "0":
            return "Unknown error"
        size = int(conn.recv(10).decode())  # 获取对方单次数据接收大小
        conn.send(file_name.encode())
        while data != b"":
            data = file.read(size)
            conn.send(data)
    except Exception as err:
        return err
    else:
        return "Send successful"
    finally:
        conn.close()
        file.close()


def recv(port=61008):
    """接收文件, 返回接收情况"""
    server = socket.socket()
    server.bind((_get_host_ip(), port))
    server.listen(1)
    conn, addr = server.accept()  # 接收请求

    data = bytes
    file = open("%s/rb.temp" % path, "wb")

    accept = yield addr  # 向函数外部主程序询问是否接收

    if not accept:  # 如果拒绝接收回调函数
        conn.send(b"1")
        return recv(port)
    else:
        conn.send(b"0")

    try:
        file_name = conn.recv(1024).decode()
        rename("rb.temp", file_name)
        conn.send(b"%d" % recv_size)  # 发送给发送端单次数据接收大小
        while data != b"":
            data = conn.recv(recv_size)
            file.write(data)
    except Exception as err:
        return err
    else:
        return "Receive successful"
    finally:
        conn.close()
        file.close()


def broadcast():
    """UDP广播, 使其他设备检测"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(b'RBC ' + username.encode(), ("<broadcast>", 60724))
    sleep(2)


def search():
    """接收UDP广播, 寻找其他设备"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 60724))
    data, addr = s.recvfrom(100)

    try:
        inform = data.decode().split()
    except (UnicodeDecodeError, UnicodeError):
        return

    if len(inform) != 2:
        return

    if inform[0] == "RBC":
        if addr[0] not in [host[0] for host in host_list]:
            host_list.append((inform[1], addr[0]))
