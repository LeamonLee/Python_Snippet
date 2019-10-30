#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""

import socket
import os
import sys
import struct


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    recvRawData = s.recv(1024)
    print(str(recvRawData))

    while 1:
        rawFilePath = input('please input file path: ')
        filepath = str(rawFilePath)
        if os.path.isfile(filepath):
            
            # Defines file information. 128s represents fine name is 128 bytes. 
            # l means int or log file type, in this case is file size
            fileinfo_size = struct.calcsize('128sl')
            print("fileinfo_size: ", fileinfo_size)
            print("os.path.basename(filepath): ", os.path.basename(filepath))
            print("os.stat(filepath).st_size: ", os.stat(filepath).st_size)

            # Defines file header information, including file name and file size
            fhead = struct.pack('128sl', bytes(os.path.basename(filepath),"utf-8"), os.stat(filepath).st_size)
            
            #print("fHead: ", str(fhead))
            print('client filepath: {0}'.format(filepath))
            s.send(fhead)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    break
                print("file content: ", data)
                s.send(data)
        s.close()
        break


if __name__ == '__main__':
    socket_client()
