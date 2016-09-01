#!/usr/bin/env python3.4

import time
from http import *
#import memcache
import http.server
import pickle
import socket
import os



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
        try:
            pickledFile = open(str(os.path.join(os.getcwd().replace('Extra_python_modules',''),'Forms',"HFHPickle")),'rb')
        except FileNotFoundError:
            print("DEBUG: Must create a new folder for forms, HTTPStaticObjData.py in Extra_python_modules")
            os.mkdir(str(os.path.join(os.getcwd().replace('Extra_python_modules',''),'Forms')))
            pickledFile = open(str(os.path.join(os.getcwd().replace('Extra_python_modules',''),'Forms',"HFHPickle")),'rb')
        shared = pickle.load(pickledFile)
        
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(b"<html><head><title>What is altered.</title></head>")
        s.wfile.write(bytes(shared,'utf-8'))
        s.wfile.write(b"</body></html>")

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
