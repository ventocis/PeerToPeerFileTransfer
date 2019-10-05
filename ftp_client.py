import socket
import sys
import socketserver

class FileListener(socketserver.BaseRequestHandler):
    def handle(self):
        print("YOOOO")

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
    if comm == "QUIT":
        break
    port = int.from_bytes(sock.recv(1024),byteorder='big',signed=False)
    print(port)
    serv = socketserver.TCPServer(('127.0.0.1', port), FileListener)
    sock.send("OK".encode('utf-8'))
    serv.handle_request()

sock.close()
