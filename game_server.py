#!/usr/bin/env python3

from lobby import Lobby

MAX_LOBBIES = 25

LOBBY_CONNECTING = 1
LOBBY_READY = 2
LOBBY_RUNNING = 3
LOBBY_CLOSED = 4


lobby_counter = 0
lobbies = []
lobby = Lobby(lobby_counter)
lobbies.append(lobby)

while True:
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

