#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 1337

# TODO:
# Recieve Commands from Zoom Python Client

# Connect to zoom clients
zoom_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
zoom_server_socket.bind((HOST, PORT))
zoom_server_socket.listen(4)

# Connect to game clients
game_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_server_socket.bind((HOST, PORT+1))
game_server_socket.listen(4)

while True:
    client_socket, addr = game_server_socket.accept()
    print("Creating connection with %s" % str(addr))
    msg = "Hello World!\n"
    client_socket.send(msg.encode('ascii'))
    client_socket.close()

# Send initial maze data to clients
def send_initial_data(client_socket):
    pass


