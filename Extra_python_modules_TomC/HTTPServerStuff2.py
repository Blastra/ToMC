#!/usr/bin/env python3.4

import http.server
import socketserver
import socket
import urllib
import os
import sys

def getExternalIP():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('google.com', 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

PORT = 8099
HOST_NAME = str(getExternalIP())

class CustomPathHandler(http.server.SimpleHTTPRequestHandler):
    
    def translate_path(self,path):
        #Find out the folder in which the script is running, go up the
        #folder path twice...
        rootPath = os.path.split(os.path.split(sys.argv[0])[0])[0]

        #Finish the path with the Worlds directory
        path = os.path.join(rootPath,"Worlds")        

        return path

Handler = CustomPathHandler

httpd = socketserver.TCPServer((HOST_NAME.replace("'",''), PORT), Handler)
httpd.serve_forever()
