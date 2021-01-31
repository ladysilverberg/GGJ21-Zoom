import socket
import select
import json
from util import read_into_buffer

MAX_PLAYERS = 4

MAZE_WIDTH = 30
MAZE_HEIGHT = 33

HOST = '127.0.0.1'
BASE_PORT = 1338

LOBBY_CONNECTING = 1
LOBBY_READY = 2
LOBBY_RUNNING = 3
LOBBY_CLOSED = 4

class Lobby:
    def __init__(self, lobby_id):
        self.lobby_id = lobby_id
        self.num_players = 0
        self.io_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.io_clients = []
        self.game_clients = []
        self.maze_walls = [
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
        self.players = [
                [4, 3],
                [17, 14],
                [6, 21],
                [27, 19]
        ]

        self.buttons = {
                (10,10):(9,18),
                (2,15):(16,15),
                (4,25):(26,3),
                (12,10):(14,15),
                (27,22):(11,4),
                (29,11):(26,23),
                (30,4):(15,16),
                (32,23):(15,14)
        }

        # Open Server Sockets
        game_port = BASE_PORT + (self.lobby_id * 2)
        io_port = BASE_PORT + (self.lobby_id * 2) + 1

        self.io_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.io_server_socket.bind((HOST, io_port))
        self.io_server_socket.listen(4)
        self.io_server_socket.setblocking(0)
        self.game_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.game_server_socket.bind((HOST, game_port))
        self.game_server_socket.listen(4)
        self.game_server_socket.setblocking(0)
        self.num_connections = 0
        self.io_connections = 0

        self.status = LOBBY_CONNECTING

    def connect_clients(self):
        read_sockets, write_sockets, error_sockets = select.select(
            [self.io_server_socket, self.game_server_socket], [], [], 0.1
        )

        for sock in read_sockets:
            # I/O Connection
            if sock is self.io_server_socket:
                io_client, addr = self.io_server_socket.accept()
                io_client.setblocking(0)
                self.io_clients.append(io_client)
                print("Lobby %s: I/O Connection %s" % (str(self.lobby_id), str(addr)))
            # Game Connection
            if sock is self.game_server_socket:
                game_client, addr = self.game_server_socket.accept()
                # game_client.setblocking(0)
                self.game_clients.append(game_client)
                print("Lobby %s: Game Connection %s" % (str(self.lobby_id), str(addr)))
                self.num_connections += 1

        if self.num_connections == MAX_PLAYERS:
            print("Lobby %s: Ready" % str(self.lobby_id))
            self.status = LOBBY_READY

    def start_game(self):
        initial_state = {
            "width": MAZE_WIDTH,
            "height": MAZE_HEIGHT,
            "maze_walls": self.maze_walls,
            "players": self.players
        }

        # Send Initial Game State to players and assigned them a player ID
        assigned_player_id = 0
        for client in self.game_clients:
            initial_state["player_id"] = assigned_player_id
            json_data = json.dumps(initial_state)
            client.send(json_data.encode('ascii'))
            assigned_player_id += 1

        print("Lobby %s: Initiated Game" % str(self.lobby_id))

        for sock in self.game_clients:
            sock.setblocking(0)

        self.status = LOBBY_RUNNING

    def update_game(self):
        # Watch for I/O
        read_sockets, write_sockets, error_sockets = select.select(self.io_clients, [], [], 0.1)
        for sock in read_sockets:
            data = sock.recv(4096)
            # Read input actions and perform them
            messages = read_into_buffer(data)
            for message in messages:
                player_id = message["player"]
                action = message["action"]
                self.game_logic(player_id, action)

            # Update cients on game state
            self.send_game_update_to_clients()

    def close(self):
        self.io_server_socket.close()
        self.game_server_socket.close()

    def game_logic(self, player_id, action):
        player = self.players[player_id]


        north = [3,6,7,10,11,12,13,15]
        south = [1,5,8,9,10,12,13,15]
        east = [4,7,8,9,11,12,14,15]
        west = [2,5,6,9,10,11,14,15]



        new_y = player[1]
        new_x = player[0]

        #movement logic
        if action == "NORTH":
            new_y -= 1
            if new_y > -1:
                value = self.maze_walls[new_y][new_x]

                if value in north:
                    player[1] = new_y

                # this is a button that was stepped on
                elif (value - 15) in north:
                    player[1] = new_y
                    self.maze_walls[new_y][new_x] -= 15

                    door_pos = self.buttons[(new_x, new_y)]
                    self.maze_walls[door_pos[0]][door_pos[1]] -= 30

        if action == "SOUTH":
            new_y += 1
            if new_y < MAZE_HEIGHT:
                value = self.maze_walls[new_y][new_x]

                if value in south:
                    player[1] = new_y

                # this is a button that was stepped on
                elif (value - 15) in south:
                    player[1] = new_y
                    self.maze_walls[new_y][new_x] -= 15

                    door_pos = self.buttons[(new_x, new_y)]
                    self.maze_walls[door_pos[0]][door_pos[1]] -= 30

        if action == "WEST":
            new_x -= 1
            if new_x > -1:
                value = self.maze_walls[new_y][new_x]

                if value in west:
                    player[0] = new_x

                # this is a button that was stepped on
                elif (value - 15) in west:
                    player[0] = new_x
                    self.maze_walls[new_y][new_x] -= 15

                    door_pos = self.buttons[(new_x, new_y)]
                    self.maze_walls[door_pos[0]][door_pos[1]] -= 30

        if action == "EAST":
            new_x += 1
            if new_x < MAZE_WIDTH:
                value = self.maze_walls[new_y][new_x]

                if (value in east):
                    player[0] = new_x

                # this is a button that was stepped on
            elif (value - 15) in east:
                    player[0] = new_x
                    self.maze_walls[new_y][new_x] -= 15

                    door_pos = self.buttons[(new_x, new_y)]
                    self.maze_walls[door_pos[0]][door_pos[1]] -= 30

        self.players[player_id] = player
        # if [victory condition for player_id]:
        #    self.num_connections -= 1 # A player has won
        #    if self.num_connections <= 0:
        #        self.status = LOBBY_CLOSED
        #        self.close() # No players left - close the lobby

        # TODO: Implement this
        pass

    def send_game_update_to_clients(self, command="update"):
        game_state = {
            "command": command,
            "maze_walls": self.maze_walls,
            "players": self.players
        }
        json_data = json.dumps(game_state)

        read_sockets, write_sockets, error_sockets = select.select(
            [], self.game_clients, [], 0.1
        )
        for sock in write_sockets:
            sock.send(json_data.encode('ascii'))

