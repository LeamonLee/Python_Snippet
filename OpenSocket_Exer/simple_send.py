#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: service.py
socket service
"""


import socket
import threading
import time
import sys


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重啟後端口被佔用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    addr = str(addr)
    print("addr: ", addr)
    print('Accepted a new connection from {0}'.format(addr))
    conn.send(bytes('Hi, Welcome to the server!', 'utf-8'))         # Must convert to bytes before sending message in python3
    while 1:
        data = conn.recv(1024)
        data = str(data)            # Must convert the data sent from client to string in python3.
        print("data: ", data)
        print('{0} client sent data {1}'.format(addr, data))
        #time.sleep(1)
        if data == 'exit' or not data:
            print('{0} connection close'.format(addr))
            conn.send('Connection closed!')
            break
        conn.send(bytes('Hello, {0}'.format(data), 'utf-8'))
    conn.close()


if __name__ == '__main__':
    socket_service()
