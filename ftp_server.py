import socket
import threading
import os
from os import listdir
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
            self.command = self.request.recv(1024).decode('utf-8')
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
                if self.command == "LIST":
                    self.list(s)
                elif self.command == "RETR":
                    self.retr(s)
                elif self.command == "STOR":
                    self.stor(s)
                elif self.command == "QUIT":
                    self.quit(s)
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

    def retr(self, s):
        print("RETR COMMAND ON PORT " + str(self.port))

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
