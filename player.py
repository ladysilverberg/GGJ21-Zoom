'''
Player object
'''

class Player:

    """A player object moves around the board, constantly updating it's x and y position"""
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_pos(self):
        return (self.y_pos, self.x_pos)
