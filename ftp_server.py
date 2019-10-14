import socket
import threading
import os
from os import listdir, path
from os.path import isfile, join

IP = '127.0.0.1'
PORT = 12000
COUNT = 0

class Client(threading.Thread):
    def __init__(self, s, addr):
        self.request = s
        self.addr = addr
        super(Client, self).__init__()

    def run(self):
        while(True):
            global COUNT
            self.command = self.request.recv(1024).decode('utf-8').split()
            print(self.command)
            COUNT = COUNT + 1
            self.port = PORT + 2 * COUNT
            print(self.port)
            self.request.send(self.port.to_bytes(8, byteorder='big'))
            ok = self.request.recv(1024).decode('utf-8')
            if ok != "OK":
                continue
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(('127.0.0.1', self.port))
                if self.command[0] == "LIST":
                    self.list(s)
                elif self.command[0] == "RETR":
                    self.retr(s, self.command)
                elif self.command[0] == "STOR":
                    print("if entered")
                    self.stor(s, self.command)
                elif self.command[0] == "QUIT":
                    self.quit(s, self.command)
                    return
                else:
                    print("Invalid command, try again.")
            except:
                print()
                continue

    def list(self, s):
        print("LIST COMMAND ON PORT " + str(self.port))
        mypath = '.'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print("Files in directory: " + str(onlyfiles))
        s.send(onlyfiles.encode('utf-8'))

    def retr(self, s, command):
        fileName = command[1]
        if path.exists(fileName):   #check if file exits
            s.send(("RETR 200 " + str(fileName)).encode('utf-8'))   #Return code 200 OK if file is found
            ourResponse = s.recv(1024).decode('utf-8')
            # f = open(fileName, "r")
            # print("Opened file " + fileName)
            # line = f.readline()
            # while line:
            #     s.send(line.encode('utf-8'))
            #     line = f.readline()
            # f.close()
            # #create TCP connection on the given client port
            # if ourResponse == "200":
            #     myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/'
            #     with open(myPath + fileName, 'r') as fs:  #Send file line by line over TCP
            #         for line in fs:
            #             s.send(line.encode('utf-8'))
                        

        myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/'
        # check if file exits
        if os.path.exists(myPath + fileName):
            # self.request.send("STOR 200".encode('utf-8'))  #Return code 200 OK if file is found
            # print("Filename:" + fileName)
            # send the file name to be downloaded
            # s.send(fileName.encode('utf-8'))
            #create TCP connection on the given client port
            with open(myPath + fileName, 'r') as fs:
                for line in fs:
                    # line = line + "\n"
                    s.send(line.encode('utf-8'))
                    ourResponse = s.recv(1024).decode('utf-8')
                s.close()
                print("File sent")




        else:
            print("File not found")
            s.send("RETR 550".encode('utf-8'))   #Return code 550 if not found
        #Terminate TCP connection

    def stor(self, s, command):
        print("stor called on server & command is:" + str(command))
        myString = "STOR "
        myString = myString + command[1]
        s.send(myString.encode('utf-8'))
        fileName = s.recv(1024).decode('utf-8')
        fileName = fileName.strip()
        f = open(fileName, "w")
        print("Created file " + fileName)
        line = s.recv(1024).decode('utf-8')
        #while line != "EOF":
        while line:
            f.write(line)
            line = s.recv(1024).decode('utf-8')
        f.close()
        print("File Downloaded")
        # print("STOR COMMAND ON PORT " + str(self.port))
        # filename = command[1]
        # if path.exists(fileName):

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
