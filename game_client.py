#!/usr/bin/python3

"""
Game Client
-------------------------------
The game client is responsible for recieving game updates from the
server and use this information to render the game from a certain
player perspective to the player.
"""

import socket
import select
import json
import sys
from maze import Maze

HOST = '127.0.0.1'
PORT = 1337
IO_PORT = 1338

# Connect to I/O Server
io_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io_socket.connect((HOST, IO_PORT))
print("Connected I/O to server")

# Connect to Game Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected Game to server")

# Recieve Initial Game State
initial_json = client_socket.recv(4096)
game_state = json.loads(initial_json.decode('ascii'))
print("Game state recieved")
client_socket.setblocking(0)

# Start Game
player_id = game_state["player_id"]
maze = Maze(game_state, player_id)
while True:
    # Non-blocking socket read
    read_sockets, write_sockets, error_sockets = select.select([client_socket], [], [], 0.1)
    for sock in read_sockets:
        data = sock.recv(4096);
        json_data = json.loads(data)
        cmd = json_data["command"]
        if cmd == "quit":
            io_socket.close()
            client_socket.close()
            exit()
        elif cmd == "update":
            maze.move_players(json_data)
        elif cmd == "victory":
            # Do game victory magic here
            pass

    # Render Maze
    maze.draw_board()
