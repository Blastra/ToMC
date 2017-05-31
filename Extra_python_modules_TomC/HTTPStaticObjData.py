#!/usr/bin/env python3.4

import time
from http import *
#import memcache
import http.server
import pickle
import socket
import os
import sys


def getExternalIP():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('google.com', 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

HOST_NAME = str(getExternalIP())

PORT_NUMBER = 9001

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):        
        #TODO: Adjust file path for different operating systems
        
        rootPath = os.path.split(os.path.split(sys.argv[0])[0])[0]
        #print("ROOTPATH: "+rootPath)
        dirPath = os.path.join(os.path.split(rootPath)[0],"HostingDataForms")
        #print("DIRPATH: "+dirPath)
        targetPath = os.path.join(rootPath,'HostingDataForms',"Storage")
        #print("Trying to find forms folder in the path: "+str(os.path.join(os.getcwd().replace('Extra_python_modules',''),'HostingDataForms',"HFHPickle")))
        #print("Trying to find HostingDataForms folder in the path: "+targetPath)
        if os.path.exists(targetPath):
            pickledFile = open(targetPath,'rb')            
        else:
            print("DEBUG: Must create a new folder for forms, HTTPStaticObjData.py in Extra_python_modules")
            os.mkdir(dirPath)
            pickledFile = open(targetPath,'wb')
            pickledFile.close()
            pickledFile = open(targetPath,'rb')
        try:
            shared = pickle.load(pickledFile)
            
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write(b"<html><head><title>What is altered.</title></head>")
            s.wfile.write(bytes(shared,'utf-8'))
            s.wfile.write(b"</body></html>")
        except EOFError:
            print("Ran out of input in static object data.")

if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME.replace("'",''), PORT_NUMBER), MyHandler)
    #print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    #print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))