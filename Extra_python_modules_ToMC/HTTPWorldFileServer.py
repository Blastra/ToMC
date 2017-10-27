#!/usr/bin/env python3.5

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

PORT = 8099

rootPath = os.path.split(os.path.split(sys.argv[0])[0])[0]
path = os.path.join(rootPath,"Worlds")
os.chdir(path)

Handler = http.server.SimpleHTTPRequestHandler

Handler.extensions_map.update({
    '.webapp': 'application/x-web-app-manifest+json',
});


httpd = socketserver.TCPServer((HOST_NAME, PORT), Handler,bind_and_activate=False)
httpd.allow_reuse_address = True
httpd.server_bind()
httpd.server_activate()

#print("Serving at port "+ str(PORT))
httpd.serve_forever()


"""
class CustomPathHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        
        pickledFile = open(os.path.join(rootPath,"Worlds",'HFHGround.dir'),'rb')
        shared = pickle.load(pickledFile)
        
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(b"<html><head><title>World repository.</title></head>")
        s.wfile.write(bytes(shared,'utf-8'))
        s.wfile.write(b"</body></html>")

    
    def translate_path(self,path):
        #Find out the folder in which the script is running, go up the
        #folder path twice...
        rootPath = os.path.split(os.path.split(sys.argv[0])[0])[0]

        #Finish the path with the Worlds directory
        path = os.path.join(rootPath,"Worlds")        

        return path

Handler = CustomPathHandler

httpd = socketserver.TCPServer((HOST_NAME.replace("'",''), PORT), Handler, bind_and_activate=False)
httpd.allow_reuse_address = True
httpd.server_bind()
httpd.server_activate()
httpd.serve_forever()
"""
