#!/usr/bin/env python3.4

import http.server
import socketserver
import socket
import urllib
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

PORT = 9002

rootPath = os.path.split(os.path.split(sys.argv[0])[0])[0]
path = os.path.join(rootPath,"ObjectLibrary")
os.chdir(path)

Handler = http.server.SimpleHTTPRequestHandler

Handler.extensions_map.update({
    '.webapp': 'application/x-web-app-manifest+json',
});


httpd = socketserver.TCPServer(("", PORT), Handler,bind_and_activate=False)
httpd.allow_reuse_address = True
httpd.server_bind()
httpd.server_activate()

print("Serving at IP "+str(HOST_NAME)+" port "+ str(PORT))
httpd.serve_forever()
