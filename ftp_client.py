import socket
import sys
import socketserver

class FileListener(socketserver.BaseRequestHandler):
    def retr(self, command):
        if command[1] == "200":
            fileName = self.request.recv(1024).decode('utf-8').strip()
            f = open(fileName, "w")
            print("Created file " + fileName)
            line = self.request.recv(1024).decode('utf-8').strip()
            #while line != "EOF":
            while line:
                f.write(line)
                line = self.request.recv(1024).decode('utf-8').strip()
            f.close()
            print("File Downloaded")
        elif command[1] == "550":
            print("File not found")
    def handle(self):
        command = self.request.recv(1024).decode('utf-8').split()
        if command[0] == "RETR":
            self.retr(command)
            

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

