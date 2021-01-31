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

# Read Arguments
if len(sys.argv) != 2:
    print("Usage: game_client.py [player_id]")
    exit()
player_id = int(sys.argv[1])

# Connect to Game Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to server")
print("Recieving initial game state...")

# Recieve Initial Game State
initial_json = client_socket.recv(4096)
game_state = json.loads(initial_json.decode('ascii'))
print("Game state recieved")
client_socket.close()

# Start Game
maze = Maze(game_state, player_id)
while True:
    # Non-blocking socket read
    read_sockets, write_sockets, error_sockets = select.select([client_socket], [], [])
    for sock in read_sockets:
        data = sock.recv(4096);
        json_data = json.loads(data)
        cmd = json_data["command"]
        if cmd == "quit":
            client_socket.close()
            exit()
        elif cmd == "update":
            maze.move_players(json_data)
        elif cmd == "victory":
            # Do game victory magic here
            pass

    # Render Maze
    maze.draw_board()
