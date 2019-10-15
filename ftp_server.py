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
            if self.command[0] == "QUIT":
                    self.quit()
                    return
            self.port = int(self.command[0])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            try:
                s.connect((IP, self.port))
                if self.command[1] == "LIST":
                    self.list(s)
                elif self.command[1] == "RETR":
                    self.retr(s, self.command)
                elif self.command[1] == "STOR":
                    self.stor(s, self.command)
                else:
                    print("Invalid command, try again.")          
            except socket.error as exc:
                print("Connection error: " + str(exc))

    def list(self, s):
        mypath = '.'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print("Files in directory: " + str(onlyfiles))
        files = "LIST " + " ".join(onlyfiles)
        s.send(files.encode('utf-8'))

    def retr(self, s, command):
        fileName = command[2]
        #myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/'
        if path.exists(fileName):   #check if file exits
            s.send(("RETR 200 " + str(fileName)).encode('utf-8'))   #Return code 200 OK if file is found
            ourResponse = s.recv(1024).decode('utf-8')
        if os.path.exists(fileName):
            with open(fileName, 'r') as fs:
                for line in fs:
                    s.send(line.encode('utf-8'))
                    ourResponse = s.recv(1024).decode('utf-8')
                s.close()
                print("File sent")    
        else:
            print("File not found")
            s.send("RETR 550".encode('utf-8'))   #Return code 550 if not found
            s.close()

    def stor(self, s, command):
        fileName = command[2].strip()
        myString = "STOR "
        myString = myString + fileName
        s.send(myString.encode('utf-8'))
        f = open(fileName, "w")
        print("Created file " + fileName)
        line = s.recv(1024).decode('utf-8')
        while line:
            f.write(line)
            line = s.recv(1024).decode('utf-8')
        f.close()
        print("File Downloaded")

    def quit(self):
        print(IP + " Has Disconnected")
        self.request.close()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))
serv.listen(1)

while True:
    conn, addr = serv.accept()
    print("USER: " + str(addr) + " CONNECTED")
    client_thr = Client(conn, addr)
    client_thr.start()
