from player import Player
import pygame
import numpy
import os

'''Server sends a json file to me (client) that I can read for all info'''
IMG_SIZE = 64
VISION = 5

class Maze:
    def __init__(self):
        # Load Images
        self.images = {}
        filenames = os.listdir("images/")
        for filename in filenames:
            img = pygame.image.load("images/" + filename)
            if filename[0] == "P":
                index = filename[0:2]
            elif filename[0] == "A":
                index = filename
            else:
                index = int(filename.split(".")[0])
            self.images[index] = img

        # Initialize PyGame
        pygame.init()
        pygame.display.set_caption("Lost")
        self.display = pygame.display.set_mode((VISION * IMG_SIZE, VISION * IMG_SIZE))
        self.display.fill((0,0,0))

    def init_game(self, game_state, player_index):
        self.height = game_state["height"]
        self.width = game_state["width"]

        self.buttons = {
                (10,10):(9,18),
                (2,15):(16,15),
                (4,25):(26,3),
                (12,10):(14,15),
                (27,23):(11,4),
                (29,11):(26,19),
                (30,4):(15,16),
                (32,24):(15,14)
        }

        self.buttons_array = [(10,10),(2,15),(4,25),(12,10),(27,23),(29,11),(30,4),(32,24)]

        self.buttons_pressed = [0,0,0,0,0,0,0,0]

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

        self.players = []
        for pos in game_state["players"]:
            player = Player(pos[0], pos[1])
            self.players.append(player)

        self.player_index = player_index

        pygame.mixer.init()
        pygame.mixer.music.load("audio/okay_zoomer.ogg")
        pygame.mixer.music.play()

    def draw_title_screen(self):
        self.display.blit(self.images["ALIZ_title.png"], (0, 0))
        pygame.display.update()

    def draw_loading_screen(self):
        self.display.blit(self.images["ALIZ_instructions.png"], (0, 0))
        pygame.display.update()

    def draw_victory_screen(self):

        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.load("audio/okay_winner.ogg")
        pygame.mixer.music.play()

        self.display.blit(self.images["ALIZ_win.png"], (0,0))
        pygame.display.update()

    def move_players(self, data):
        buttons_pressed = data["buttons_pressed"]

        for i in range(len(buttons_pressed)):
            if self.buttons_pressed[i] != buttons_pressed[i]:
                button = self.buttons_array[i]
                door = self.buttons[button]
                self.maze_walls[button[0]][button[1]] -= 15
                self.maze_walls[door[0]][door[1]] -= 30

                self.buttons_pressed[i] = buttons_pressed[i]

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
                    for i in range(len(self.players)):
                        player = self.players[i]
                        if player.get_pos() == (array_y, array_x):
                            index = "P" + str(i+1)
                            self.display.blit(self.images[index], img_pos)
        pygame.display.update()
