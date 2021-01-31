#!/usr/bin/env python3

import socket
import select
import json

HOST = '127.0.0.1'
PORT = 1337     # Game Socket Port
IO_PORT = 1338  # I/O Socket Port
NUM_PLAYERS = 1

maze_state = [
    [6,7,0,6,14,7,0,6,14,14,14,7,0,6,4,0,3,0,0,0,0,6,14,14,14,14,14,14,7,0],
    [13,5,14,8,0,13,0,13,0,0,0,13,0,13,0,0,5,14,14,14,11,9,14,4,0,0,0,0,13,0],
    [13,0,0,0,0,13,0,5,7,0,6,8,0,13,0,18,0,0,0,0,13,0,0,0,0,0,6,14,8,0],
    [13,0,6,14,14,8,0,0,13,0,13,0,6,8,0,5,11,14,7,0,5,14,14,7,0,0,13,0,0,0],
    [13,0,13,0,0,0,0,0,13,0,13,0,13,0,0,0,13,0,13,0,0,0,0,13,0,17,15,14,7,0],
    [13,0,5,14,14,14,14,14,12,0,13,0,5,7,0,0,13,0,5,14,14,7,0,13,0,0,1,0,13,0],
    [13,0,0,0,0,0,0,0,13,0,13,0,0,13,0,0,13,0,0,0,0,13,0,13,0,0,0,0,13,0],
    [5,14,14,7,0,6,14,14,8,0,5,11,14,8,0,0,5,7,0,6,14,8,0,5,14,14,11,14,8,0],
    [0,0,0,13,0,13,0,0,0,0,0,13,0,0,0,0,0,13,0,13,0,0,0,0,0,0,13,0,0,0],
    [2,11,14,8,0,5,14,14,7,0,0,10,14,7,0,6,14,9,41,8,0,6,14,14,7,0,5,7,0,0],
    [0,13,0,0,0,0,0,0,13,0,17,8,0,13,0,13,0,0,13,0,0,13,0,0,13,0,0,5,14,7],
    [0,5,14,14,41,14,14,14,12,0,0,0,0,13,0,13,0,6,8,0,0,13,0,0,13,0,0,0,0,13],
    [3,0,0,0,13,0,0,0,1,0,18,0,0,5,7,13,0,13,0,0,6,9,4,0,5,14,11,14,14,12],
    [13,0,3,0,13,0,0,0,0,0,13,0,0,0,13,13,0,13,0,0,13,0,0,0,0,0,13,0,0,13],
    [10,14,9,14,9,14,14,11,14,14,8,0,6,14,8,43,0,5,14,14,9,14,4,0,2,14,8,0,2,8],
    [1,0,0,0,0,0,0,1,0,0,0,0,5,14,44,15,44,14,14,7,0,0,0,0,6,14,14,14,14,7],
    [0,0,0,0,0,0,0,0,0,0,0,0,6,14,7,43,0,0,0,13,0,0,0,0,13,0,0,0,0,13],
    [6,14,7,0,0,3,0,6,14,14,14,14,8,0,5,8,6,14,14,8,0,0,6,14,8,0,6,14,14,8],
    [13,0,13,0,0,13,0,13,0,0,0,0,0,0,0,0,13,0,0,0,0,0,13,0,0,0,13,0,0,0],
    [13,0,10,14,14,8,0,5,14,11,14,14,14,14,7,0,13,0,6,14,14,14,9,14,4,0,5,14,7,0],
    [13,0,13,0,0,0,0,0,0,13,0,0,0,0,13,0,13,0,13,0,0,0,0,0,0,0,0,0,13,0],
    [13,0,5,14,14,11,14,14,14,9,14,7,0,0,13,0,5,11,8,0,0,6,14,14,7,0,0,0,13,0],
    [13,0,0,0,0,13,0,0,0,0,0,13,0,0,5,7,0,13,0,2,14,12,0,0,13,0,2,14,12,0],
    [5,14,14,7,0,13,0,0,0,0,0,1,0,0,0,13,0,13,0,0,0,1,0,0,13,0,0,0,13,0],
    [0,0,0,13,0,5,14,11,14,4,0,0,0,0,0,13,0,5,14,7,0,0,2,14,15,14,14,14,8,0],
    [0,0,0,13,0,0,0,13,0,0,0,0,0,0,2,8,0,0,0,13,0,0,0,0,13,0,0,0,0,0],
    [6,14,14,39,14,7,0,13,0,0,6,14,14,7,0,0,0,3,0,40,14,7,0,0,10,14,14,14,14,7],
    [13,0,0,0,0,13,0,5,14,14,8,0,0,13,0,3,0,10,14,8,0,13,0,17,8,0,0,0,0,13],
    [5,14,11,4,0,13,0,0,0,0,0,0,0,10,14,12,0,13,0,0,0,13,0,0,0,0,0,0,0,13],
    [0,0,13,0,0,5,14,14,14,7,0,18,0,1,0,13,0,5,11,4,0,5,14,11,14,14,4,0,0,13],
    [6,14,8,0,18,0,0,0,0,13,0,13,0,0,0,13,0,0,13,0,0,0,0,13,0,0,0,6,14,8],
    [13,0,0,0,5,7,0,6,14,15,14,9,14,14,14,9,14,14,15,14,14,4,0,13,0,2,14,12,0,0],
    [5,14,14,14,14,8,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,5,19,0,0,5,14,4]
]

players = [
    [4, 3],
    [17, 14],
    [6, 21],
    [27, 19]
]

# Initial Game State send to clients
initial_game_state = {
    "height": 33,
    "width": 30,
    "maze_walls": maze_state,
    "players": players
}
initial_json = json.dumps(initial_game_state)

def send_game_update(clients, command):
    game_state = {
        "command": command,
        "maze_walls": maze_state,
        "players": players
    }
    json_data = json.dumps(game_state)
    for client in clients:
        client.send(json_data.encode('ascii'))

# Connect to I/O clients
io_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io_server_socket.bind((HOST, IO_PORT))
io_server_socket.listen(4)

io_clients = []
num_clients = 0
while num_clients < NUM_PLAYERS:
    io_client_socket, addr = io_server_socket.accept()
    print("Connecting w/ IO Client on %s" % str(addr))
    io_clients.append(io_client_socket)
    num_clients += 1

# Connect to game clients
game_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_server_socket.bind((HOST, PORT))
game_server_socket.listen(4)

clients = []
num_clients = 0
while num_clients < NUM_PLAYERS:
    client_socket, addr = game_server_socket.accept()
    print("Connecting w/ Game Client on %s" % str(addr))
    clients.append(client_socket)
    num_clients += 1

# Send Initial Game State to Clients
for client in clients:
    client.send(initial_json.encode('ascii'))

print("Sent game state to all client")
game_server_socket.close()

def game_server_logic(player_id, action):
    pass

# Listen to I/O Commands
while True:
    read_sockets, write_sockets, error_sockets = select.select(io_clients, [], [])
    for sock in read_sockets:
        data = sock.recv(2048)
        json_data = json.loads(data)
        player_id = json_data["player"]
        action = json_data["action"] # move_up, move_down, quit etc.
        if action == "quit":
            io_server_socket.close()
            game_server_socket.close()
            exit()
        game_server_logic(player_id, action)

