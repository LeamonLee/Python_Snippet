# import http.server
# import socketserver

# PORT = 8000
# Handler = http.server.SimpleHTTPRequestHandler
# httpd = socketserver.TCPServer(("",PORT), Handler)
# print("Server started at PORT : ", PORT)

# httpd.serve_forever()

# ========================================================

# from socketserver import StreamRequestHandler                    #选择 TCP的处理器类
# import socketserver
# HOST =''
# PORT = 8888
# addr = (HOST, PORT)

# '''处理器类部分'''
# class myTcpFileServer(StreamRequestHandler):                          #第二步：自定义处理器类的功能(这也是一个请求--request)
#     def handle(self):
#         print('client\'s address:',self.client_address)              #打印连接上的客户端的 ip地址
#         self.request.sendall(bytes("Hello this is from socketFileServer", "utf-8"))
#         while True:
#             data = self.request.recv(1024)                      #从客户端接收信息
#             if not data:
#                 break
#             print(data.decode('utf-8'))
#             self.request.sendall(data)                          #向客户端发送信息

# if __name__ == '__main__':
#     '''服务器类部分'''
#     server = socketserver.TCPServer(addr, myTcpFileServer)      #第一步：.选择一个服务器类，并创建其对象
#     print("Server started at PORT : ", PORT)
#     server.serve_forever()                                      #第三步：开启服务器

# ========================================================

#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""

import os
import sys
import cgi
import http
import mimetypes
import threading
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler



class CORSRequestHandler(SimpleHTTPRequestHandler):
    def _set_headers(self, ext):
        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.send_header('Content-type', 'text/plain')
        _mimetype, _ = mimetypes.guess_type(ext)
        print("_mimetype: ", _mimetype)
        self.send_header('Content-type', _mimetype)
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)
        # self.end_headers()

    def do_GET(self):
        self._set_headers(ext=self.path)
        # print("os.curdir: ", os.curdir)
        # print("os.sep: ", os.sep)
        print("self.path: ", self.path)
        filepath = str(os.curdir + os.sep + self.path)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as fp:
                # while True:
                # data = fp.read(1024)
                data = fp.read()
                if not data:
                    print('{0} file sent over...'.format(filepath))
                    # break
                # print("file content: ", data)
                # s.send(data)
                self.wfile.write(data)
        else:
            self.wfile.write(("mini Python Server is working...\nPlease input correct filename.").encode())   # should be bytes
            

    def do_POST(self):
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {'REQUEST_METHOD': 'POST'}
        )

        # 获取 POST 过来的 Value
        value = form.getvalue("key")

        self._set_headers()
        self.wfile.write(value.encode())


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """


def run(server_class=HTTPServer, handler_class=CORSRequestHandler, port=8081):
    server_address = ('', port)
    ThreadedHTTPServer.allow_reuse_address = True                   # Leamon added
    httpd = ThreadedHTTPServer(server_address, handler_class)
    httpd.daemon_threads = True                                     # Leamon added
    print('Starting httpd on 8081...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        httpd.server_close()
        print("Disconnected")
        sys.exit(0)

    except Exception as e:
        print("Exception occurred")
        print(e)


if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()