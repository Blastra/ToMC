import os

#Obtain the IP file's path

upperIPpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')) #,os.path.join('Configurations','LocalMachineIPs.txt'))
fullIPpath = os.path.join(upperIPpath,"Configurations","LocalMachineIPs.txt")

IPFile = open(fullIPpath,'r')

#Read the first line, which contains the local external IP address
IPLump = IPFile.readlines()

#Pick out the local network IP for use in HTTP server functions
#Remove the newline symbols as well
IP = IPLump[0].rstrip()

#Close the file
IPFile.close()

