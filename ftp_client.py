import socket
import sys
import socketserver
import re

class FileListener(socketserver.BaseRequestHandler):
    def handle(self):
        print("handle file input here")

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
count = 0
dPort = 140000

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
    # count = count + 1
    # dPort = dPort + count * 2
    # comm = comm + " " + str(dPort)
    sock.send(comm.encode('utf-8'))
    port = int.from_bytes(sock.recv(1024),byteorder='big',signed=False)
    print(port)
    serv = socketserver.TCPServer(('127.0.0.1', port), FileListener)
    sock.send("OK".encode('utf-8'))
    serv.handle_request()
    if comm == "QUIT":
        print("CLOSING CONNECTION...GOODBYE")
        break
    if re.search('STORE .*', comm) is not None:
        storSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        storSoc.bind(('127.0.0.1', port))
        storSoc.listen()
        storSoc.accept()
		# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# s.connect((TCP_IP, TCP_PORT))
		# s.send(MESSAGE)
		# data = s.recv(BUFFER_SIZE)
		# s.close()
        print("good")

        # sock.send("check")


sock.close()

#1) open data port as server
#2)wait for response from server
#3) Send file
#4)close connection
