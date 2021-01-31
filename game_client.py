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
from util import read_into_buffer

HOST = '158.39.200.234'
MGMT_PORT = 1337
BASE_PORT = 1338

# Connect to management to get delegated a lobby port
lobby_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lobby_socket.connect((HOST, MGMT_PORT))
print("Connected to Lobby")
print("Waiting for lobby delegation...")
json_data = lobby_socket.recv(4096)
lobby_data = json.loads(json_data.decode('ascii'))
lobby_id = lobby_data["lobby_id"]
lobby_socket.close()
print("Assigned to Lobby %s" % str(lobby_id))
game_port = BASE_PORT + (lobby_id * 2)
io_port = BASE_PORT + (lobby_id * 2) + 1

print(io_port)

# Show title screen
maze = Maze()
running = True
while running:
    inp = maze.get_input()
    if "SPACE" in inp:
        running = False
    maze.draw_title_screen()

# Connect to I/O Server
io_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io_socket.connect((HOST, io_port))
print("Connected I/O to server")

# Connect to Game Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, game_port))
print("Connected Game to server")

# Show instructions screen / waiting screen
maze.draw_loading_screen()

# Recieve Initial Game State
initial_json = client_socket.recv(4096)
game_state = json.loads(initial_json.decode('ascii'))
print("Game state recieved")
client_socket.setblocking(0)

player_id = game_state["player_id"]
# Start Game
maze.init_game(game_state, player_id)
running = True
while running:

    # Non-blocking socket read
    read_sockets, write_sockets, error_sockets = select.select([client_socket], [], [], 0.1)
    for sock in read_sockets:
        data = sock.recv(4096)
        try:
            messages = read_into_buffer(data)
            for message in messages:
                cmd = message["command"]
                if cmd == "update":
                    maze.move_players(message)
                elif cmd == "victory":
                    running = False
                    break
        except Exception as e:
            print(e)
    # Send input to server
    action = maze.get_input()
    if "NONE" not in action:
        json_data = json.dumps({"player":player_id, "action": action})
        io_socket.send(json_data.encode('ascii'))

    # Render Maze
    maze.draw_board()

while True:
    inp = maze.get_input()
    maze.draw_victory_screen()
    if inp == "SPACE":
        break

io_socket.close()
client_socket.close()
