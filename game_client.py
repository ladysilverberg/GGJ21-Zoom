#!/usr/bin/python3

import socket

HOST = '127.0.0.1'
PORT = 1337

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

msg = client_socket.recv(1024)
client_socket.close()

print(msg.decode('ascii'))
