import socket
import threading
import os
from os import listdir, path
from os.path import isfile, join

IP = '127.0.0.1'
PORT = 12000

class Client(threading.Thread):
    def __init__(self, s, addr):
        self.request = s
        self.addr = addr
        super(Client, self).__init__()

    def run(self):
        while(True):
            self.command = self.request.recv(1024).decode('utf-8').split()
            self.port = int(self.command[0])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            try:
                s.connect((IP, self.port))
                if self.command[1] == "LIST":
                    self.list(s)
                elif self.command[1] == "RETR":
                    self.retr(s, self.command)
                elif self.command[1] == "STOR":
                    self.stor(s)
                elif self.command[1] == "QUIT":
                    self.quit(s)
                    return
                else:
                    print("Invalid command, try again.")          
            except socket.error as exc:
                print("Connection error: " + str(exc))

    def list(self, s):
        print("LIST COMMAND ON PORT " + str(self.port))
        mypath = '.'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print("Files in directory: " + str(onlyfiles))
        s.send(onlyfiles.encode('utf-8'))

    def retr(self, s, command):
        fileName = command[2]
        if path.exists(fileName):   #check if file exits
            s.send("RETR 200".encode('utf-8'))   #Return code 200 OK if file is found
            s.send(fileName.encode('utf-8'))    #send the file name to be downloaded
            with open(fileName, 'r') as fs: #Send file line by line over TCP
                line = fs.read(1024)
                while line:
                    s.send(line.encode('utf-8'))
                    line = fs.read(1024)
                s.close()
                print("File sent")   
        else:
            print("File not found")
            s.send("RETR 550".encode('utf-8'))   #Return code 550 if not found
        #Terminate TCP connection

    def stor(self, s):
        print("STOR COMMAND ON PORT " + str(self.port))

    def quit(self, s):
        print("QUIT COMMAND ON PORT " + str(self.port))
        print("CLOSING SOCKET... GOODBYE")
        s.close()
        self.request.close()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))
serv.listen(1)

while True:
    conn, addr = serv.accept()
    print("USER: " + str(addr) + " CONNECTED")
    client_thr = Client(conn, addr)
    client_thr.start()
