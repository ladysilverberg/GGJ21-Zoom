import socket
import select
import json

MAX_PLAYERS = 4

MAZE_WIDTH = 30
MAZE_HEIGHT = 33

HOST = '127.0.0.1'
GAME_PORT = 1337
IO_PORT = 1338

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
        
        # Open Server Sockets
        self.io_server_socket.bind((HOST, IO_PORT))
        self.io_server_socket.listen(4)
        self.io_server_socket.setblocking(0)
        self.game_server_socket.bind((HOST, GAME_PORT))
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
        self.status = LOBBY_RUNNING

    def update_game(self):
        # Watch for I/O
        read_sockets, write_sockets, error_sockets = select.select(self.io_clients, [], [], 0.1)
        for sock in read_sockets:
            data = sock.recv(4096)
            json_data = json.loads(data)
            player_id = json_data["player"]
            action = json_data["action"]
            self.game_logic(player_id, action)

    def close(self):
        self.io_server_socket.close()
        self.game_server_socket.close()

    def game_logic(self, player_id, action):
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
        for client in self.game_clients:
            client.send(json_data.encode('ascii'))

