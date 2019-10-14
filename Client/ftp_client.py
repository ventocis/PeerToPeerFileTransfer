import socket
import sys
import socketserver
from os import listdir, path
from os.path import isfile, join
import os

class FileListener(socketserver.BaseRequestHandler):
    def retr(self, command):
         if command[1] == "200":
                fileName = self.request.recv(1024).decode('utf-8')
                with open(fileName, 'w') as f:     
                    line = self.request.recv(1024).decode('utf-8')
                    while line != "eof":
                        print(line)
                        f.write(line)
                        line = self.request.recv(1024).decode('utf-8')

    def stor(self, command):
        print("stor called on client & command is:" + str(command))
        fileName = command[1]
        print("filename:" + fileName)
        fileName = fileName.strip()
        myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/Client/'
        # check if file exits
        if os.path.exists(myPath + fileName):
            # self.request.send("STOR 200".encode('utf-8'))  #Return code 200 OK if file is found
            print("Filename:" + fileName)
            self.request.send(fileName.encode('utf-8'))    #send the file name to be downloaded
            #create TCP connection on the given client port
            with open(myPath + fileName, 'r') as fs:
                for line in fs:
                    # line = line + "\n"
                    self.request.send(line.encode('utf-8'))
                self.request.close()
                print("File sent")

            # with open(myPath + fileName, 'r') as fs: #Send file line by line over TCP 
            #     line = fs.read(1024)
            #     while line:
            #         self.request.send(line.encode('utf-8'))
            #         line = fs.read(1024)
            #     self.request.close()
            #     print("File sent")


        else:
            self.send("STOR 550".encode('utf-8'))   #Return code 550 if not found
        #Terminate TCP connection

    def handle(self):
        print("handle file input here")
        command = self.request.recv(1024).decode('utf-8').split()
        print(command)
        if command[0] == "RETR":
            self.retr(command)
        elif command[0] == "STOR":
            print("got to handle")
            self.stor(command)
        else:
            print("Skipped it")
        return 
            

print("Welcome to our FTP Client!")
print("Commands")
print("CONNECT [ADDRESS] [PORT]: connects you to a server")
print("LIST: lists files on server")
print("RETR [FILENAME]: retrieves file on server")
print("STOR [FILENAME]: stores file on server")
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
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip,port))
        except:
            print("ERROR: Invalid IP or port")
            continue
        break
    else:
        print("MUST CONNECT BEFORE USING OTHER COMMANDS")
        continue

while True:
    comm = input("INPUT COMMAND: ")
    sock.send(comm.encode('utf-8'))
    port = int.from_bytes(sock.recv(1024),byteorder='big',signed=False)
    print(port)
    serv = socketserver.TCPServer(('127.0.0.1', port), FileListener)
    sock.send("OK".encode('utf-8'))
    serv.handle_request()
    comm = comm.split()
    if comm[0] == "QUIT":
        print("CLOSING CONNECTION...GOODBYE")
        break

sock.close()



