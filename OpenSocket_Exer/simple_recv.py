#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: client.py
socket client
"""

import socket
import sys


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
        print("Connected successfully")
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024))
    while 1:
        data = input('please input something: ')
        byteInputMsg = bytes(data, 'utf-8')             # Must convert to bytes before sending message in python3
        # s.send(data)
        s.send(byteInputMsg)
        recvData = s.recv(1024)                        # Must convert the data sent from client to string in python3.
        print(str(recvData))
        if data == 'exit':
            break
    s.close()


if __name__ == '__main__':
    socket_client()
