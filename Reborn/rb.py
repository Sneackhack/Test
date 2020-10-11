#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os import mkdir, _exit
from os.path import exists
from sys import argv, exit
from threading import Thread
from time import sleep

from lib.conf import path, recv_port, send_port
from lib.network import send, recv, broadcast, search, host_list

args = argv[1:]


class _RecvThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.result = ""

    def start(self):
        self.result = recv(recv_port)


if not args or "help" in args:  # 检查是否输出帮助文档
    with open("data/resources/help.txt") as help_file:
        print(help_file.read())
    exit()

if args[0] == "send":
    file_path = args[1]
    if not exists(file_path):
        print("No such file or directory")
    result = send(file_path, args[2], send_port)
    print(result)  # 输出发送结果

if args[0] == "recv":
    if not exists(path):
        mkdir(path)
    recv_thread = _RecvThread()
    try:
        while not recv_thread.result:
            broadcast()
    except KeyboardInterrupt:
        _exit(0)
    else:
        print(recv_thread.result)

if args[0] == "search":
    text = "Username                       IP Address\n"
    Thread(target=search).start()
    try:
        sleep(int(args[1]) if len(args) >= 2 else 20)
    except:
        for host in host_list:
            text += "%-30s %s" % host
        print(text)
        _exit(0)

    for host in host_list:
        text += "%-30s %s\n" % host
    print(text)
    _exit(0)
