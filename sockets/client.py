import socket

"""
Build a client using a TCP socket with a
target host IP address and a target host port.
"""

HOST = "192.168.4.29" # Host of the server (Target host)
PORT = 9090 # Target port on server

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

socket.send("Hello World!".encode('utf-8'))

# msg = socket.recv(8)
# while msg:
#     print(msg.decode('utf-8'))
#     msg = socket.recv(8)

byte_size = 8 # or 1024
full_msg = ""
while True:
    msg = socket.recv(byte_size)
    if len(msg) <= 0:
        break
    full_msg += msg.decode('utf-8')

print(full_msg)