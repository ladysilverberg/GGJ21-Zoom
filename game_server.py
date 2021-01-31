#!/usr/bin/env python3

import socket
import select
import json
from lobby import Lobby

HOST = '127.0.0.1'
MGMT_PORT = 1337

MAX_LOBBIES = 25

LOBBY_CONNECTING = 1
LOBBY_READY = 2
LOBBY_RUNNING = 3
LOBBY_CLOSED = 4

# Set Up Management Socket
lobby_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lobby_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lobby_socket.bind((HOST, MGMT_PORT))
lobby_socket.listen(4)
lobby_socket.setblocking(0)

# Start Lobby System
lobby_counter = 0
lobbies = []
lobby = Lobby(lobby_counter)
lobbies.append(lobby)

# Run Lobby System
while True:
    # Check for Lobby Connections
    read_sockets, write_sockets, error_sockets = select.select(
        [lobby_socket], [], [], 0.1
    )
    for sock in read_sockets:
        lobby_conn, addr = lobby_socket.accept()
        lobby_data = {
            "lobby_id": lobby_counter
        }
        json_data = json.dumps(lobby_data)
        lobby_conn.send(json_data.encode('ascii'))

    for lobby in lobbies:
        if lobby.status == LOBBY_CONNECTING:
            lobby.connect_clients()
        elif lobby.status == LOBBY_READY:
            lobby.start_game()

            # Create New Lobby
            if lobby_counter < MAX_LOBBIES:
                lobby_counter += 1
                new_lobby = Lobby(lobby_counter)
                lobbies.append(new_lobby)
        elif lobby.status == LOBBY_RUNNING:
            lobby.update_game()
        elif lobby.status == LOBBY_CLOSED:
            lobbies.remove(lobby)
            lobby_counter -= 1
