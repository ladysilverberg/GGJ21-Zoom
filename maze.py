from player import Player
import pygame
import numpy
import os

'''Server sends a json file to me (client) that I can read for all info'''
IMG_SIZE = 64
VISION = 5

class Maze:
    def __init__(self, game_state, player_index):
        self.height = game_state["height"]
        self.width = game_state["width"]
        self.maze_walls = game_state["maze_walls"]

        self.players = []
        for pos in game_state["players"]:
            player = Player(pos[0], pos[1])
            self.players.append(player)

        self.player_index = player_index

        # Load Images
        self.images = {}
        filenames = os.listdir("images/")
        for filename in filenames:
            img = pygame.image.load("images/" + filename)
            if filename[0] == "P":
                index = filename[0:2]
            else:
                index = int(filename.split(".")[0])
            self.images[index] = img

        # Initialize PyGame
        pygame.init()
        pygame.display.set_caption("Lost")
        self.display = pygame.display.set_mode((VISION * IMG_SIZE, VISION * IMG_SIZE))
        self.display.fill((0,0,0))

        pygame.mixer.init()
        pygame.mixer.music.load("audio/zoomer.ogg")
        pygame.mixer.music.play()

    def move_players(self, data):
        self.maze_walls = data["maze_walls"]
        for i in range(len(self.players)):
            pos = data["players"][i]
            self.players[i].x_pos = pos[0]
            self.players[i].y_pos = pos[1]

    def get_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == 97:
                    return "WEST"
                if event.key == pygame.K_RIGHT or event.key == 100:
                    return "EAST"
                if event.key == pygame.K_UP or event.key == 119:
                    return "NORTH"
                if event.key == pygame.K_DOWN or event.key == 115:
                    return "SOUTH"
                if event.key == pygame.K_SPACE:
                    return "SPACE"
        return "NONE"

    def draw_board(self):
        self.display.fill((0,0,0))

        if pygame.mixer.music.get_busy() == 0:
            pygame.mixer.music.play()

        for y in range(-2, 3):
            for x in range(-2, 3):
                array_y = y + self.players[self.player_index].get_pos()[0]
                array_x = x + self.players[self.player_index].get_pos()[1]

                if array_y < self.height and array_y > -1 and array_x < self.width and array_x > -1:
                    img_pos = ((x+2)*IMG_SIZE, (y+2)*IMG_SIZE)
                    index = self.maze_walls[array_y][array_x]
                    self.display.blit(self.images[index], img_pos)
                    for player in self.players:
                        if player.get_pos() == (array_y, array_x):
                            index = "P" + str(self.player_index+1)
                            self.display.blit(self.images[index], img_pos)
        pygame.display.update()
