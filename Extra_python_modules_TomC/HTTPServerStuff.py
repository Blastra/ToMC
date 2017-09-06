#!/usr/bin/env python3.4

import time
from http import *
#import memcache
import http.server
import pickle
import socket
import os
import sys


#By now the file which contains the server's IP address
#has been created, use its contents

#Obtain the IP file's path

upperIPpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')) #,os.path.join('Configurations','LocalMachineIPs.txt'))
fullIPpath = os.path.join(upperIPpath,"Configurations","LocalMachineIPs.txt")

IPFile = open(fullIPpath,'r')

#Read the first line, which contains the local external IP address
IPLump = IPFile.readlines()

#Pick out the local network IP for use in HTTP server functions
#Remove the newline symbols as well
HOST_NAME = IPLump[0].rstrip()

#Close the file
IPFile.close()

#TODO: An easy port configuration option can be thought out as well
PORT_NUMBER = 8098

rootPath = os.path.split(os.path.split(sys.argv[0])[0])[0]

#TODO: Change the method of hosting files to apache, node or nginx
#to increase security

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        
        pickledFile = open(os.path.join(rootPath,"HostingDataForms",'Storage'),'rb')
        try:
            shared = pickle.load(pickledFile)
            #Store the sent message in case EOF occurs
            #as a result of rewriting the file being rewritten
            global storedPrevious
            storedPrevious = shared
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write(b"<html><head><title>The found world.</title></head>")
            s.wfile.write(bytes(shared,'utf-8'))
            s.wfile.write(b"</body></html>")
        except EOFError:
            print("Ran out of world data to read.")
            #Errors caused by EOFErros is causing Python script repetition
            #to be halted by RemoteDisconnected errors - storing a previous,
            #functional version of the data may be a solution
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write(b"<html><head><title>The found world.</title></head>")
            s.wfile.write(bytes(storedPrevious,'utf-8'))
            s.wfile.write(b"</body></html>")
            #httpd.server_close()
    def log_message(self, format, *args):
        return

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
