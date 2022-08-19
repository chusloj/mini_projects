import socket
import select
import errno  # match error codes
import sys

HEADER_LENGTH = 10

IP = "localhost"
PORT = 4321

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))  # connect to server
client_socket.setblocking(False)

username = my_username.encode("utf-8")

# this is just to fill the header value in the message format when the client
# sends its first message to introduce itself
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")

client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        # send message
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

    try:
        while True:
            # receive broadcasted messages
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print(f"Connection closed by the server")
                sys.exit()
            username_length = int(
                username_header.decode("utf-8").strip()
            )  # strip() used for safety
            username = client_socket.recv(username_length).decode("utf-8")
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            # print message from username
            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue  # if we get EAGAIN or EWOULDBLOCK then continue

    except Exception as e:
        print("General error", str(e))
        sys.exit()
