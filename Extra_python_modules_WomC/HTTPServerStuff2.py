#!/usr/bin/env python3.4

import http.server
import socketserver
import socket

def getExternalIP():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('google.com', 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

HOST_NAME = str(getExternalIP())


Handler = http.server.SimpleHTTPRequestHandler
 
httpd = socketserver.TCPServer((HOST_NAME.replace("'",''), 8099), Handler)
httpd.serve_forever()
