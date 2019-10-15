import socket
import sys
import socketserver
from os import listdir, path
from os.path import isfile, join
import os

PORT = 12000
COUNT = 1

class FileListener(socketserver.BaseRequestHandler):
    def retr(self, command):
        if command[1] == "200":
            #myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/Client/'
            fileName = command[2]
            fileName = fileName.strip()
            f = open(fileName, "w")
            self.request.send(("200").encode('utf-8'))
            print("Created file " + fileName)
            line = self.request.recv(1024).decode('utf-8')
            while line:
                f.write(line)
                self.request.send(("200").encode('utf-8'))
                line = self.request.recv(1024).decode('utf-8')
            f.close()
            print("File Downloaded")
        elif command[1] == "550":
            print("File not found")

    def stor(self, command):
        fileName = command[1].strip()
        #myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/Client/'
        with open(fileName, 'r') as fs:
            for line in fs:
                self.request.send(line.encode('utf-8'))
            self.request.close()
            print("File Uploaded")


    def list(self, command):
        if len(command) <= 1:
            print("No files to list")
        else:
            print("Files stored:")
            for x in command:
                if x != "LIST":
                    print("\t" + x)

    def handle(self):     
        command = self.request.recv(1024).decode('utf-8').split()
        if command[0] == "RETR":
            self.retr(command)
        elif command[0] == "STOR":
            self.stor(command)
        elif command[0] == "LIST":
            self.list(command)
        else:
            print("Skipped it")
        return 

def setupSocket(command):
    global PORT
    global COUNT
    PORT = PORT + 2 * COUNT
    command = str(PORT) + " " + command
    serv = socketserver.TCPServer(('127.0.0.1', PORT), FileListener)
    sock.send(command.encode('utf-8'))
    serv.handle_request()

def retr(command):
    setupSocket(command)

def stor(command):
    tokens = command.split()
    fileName = tokens[1].strip()
    if os.path.exists(fileName):
        print("File " + fileName + " found")
        setupSocket(command)
    else:
        print("File Not Found")

def listCMD(command):
    setupSocket(command)

print("Welcome to our FTP Client!")
print("Commands")
print("CONNECT [ADDRESS] [PORT]: connects you to a server")
print("LIST: lists files on server")
print("RETR [FILENAME]: retrieves file on server")
print("STORE [FILENAME]: stores file on server")
print("QUIT: closes connection with server and exits the program")
print()

ip = None
port = None
sock = None
while True:
    comm = input("INPUT COMMAND: ")
    tokens = comm.split()
    if tokens[0] == "CONNECT":
        if len(tokens) != 3:
            print("INCORRECT NUMBER OF ARGUMENTS")
            continue
        ip = tokens[1]
        port = int(tokens[2])
        if port != 12000:
            print("INCORRECT PORT")
            continue
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip,port))
            print("Connected to " + ip)
        except:
            print("ERROR: Invalid IP or port")
            continue
        break
    else:
        print("MUST CONNECT BEFORE USING OTHER COMMANDS")
        continue

while True:
    comm = input("\nINPUT COMMAND: ")
    tokens = comm.split()
    if tokens[0] == "RETR" and len(tokens) == 2:
        retr(comm)
    elif tokens[0] == "STOR" and len(tokens) == 2:
        stor(comm)
    elif tokens[0] == "LIST" and len(tokens) == 1:
        listCMD(comm)
    elif tokens[0] == "QUIT" and len(tokens) == 1:
        sock.send(comm.encode('utf-8'))
        print("CLOSING CONNECTION TO SERVER...GOODBYE")
        sys.exit()
    else:
        print("Invalid Command")

sock.close()

