#!/usr/bin/python3

"""
I/O Client
-------------------------------
The I/O client is responsible for reading player input,
parsing this as commands and send it to the server.
"""

import socket
import select
import json

HOST = '127.0.0.1'
PORT = 1338

# Read Arguments
if len(sys.argv) != 2:
    print("Usage: io_client.py [player_id]")
    exit()
player_id = int(sys.argv[1])

# Connect to Game Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to server")
client_socket.close()

# Logic for reading input goes here...

# Send I/O Message
#action = "move_up"
#io_msg = {
#    "player_id": player_id,
#    "action": action
#}
