north = [3,6,7,10,11,12,13,15]
south = [1,5,8,9,10,12,13,15]
east = [4,7,8,9,11,12,14,15]
west = [2,4,6,9,10,11,14,15]

def move_player(self, player, direction):
    player.y_pos = new_y
    player.x_pos = new_x

    if direction == "north":
        new_y -= 1
        if new_y > -1:
            value = maze_walls[new_y][new_x]

            if value in north:
                player.y_pos = new_y

            # this is a button that was stepped on
            elif (value - 15) in north:
                player.y_pos = new_y
                maze_walls[new_y][new_x] -= 15

                door_pos = buttons[(new_x, new_y)]
                maze_walls[door_pos[0]][door_pos[1]] -= 30

    if direction == "south":
        new_y += 1
        if new_y < height:
            value = maze_walls[new_y][new_x]

            if value in south:
                player.y_pos = new_y

            # this is a button that was stepped on
        elif (value - 15) in south:
                player.y_pos = new_y
                maze_walls[new_y][new_x] -= 15

                door_pos = buttons[(new_x, new_y)]
                maze_walls[door_pos[0]][door_pos[1]] -= 30

    if direction == "west":
        new_x -= 1
        if new_x > -1:
            value = maze_walls[new_y][new_x]

            if value in west:
                player.x_pos = new_x

            # this is a button that was stepped on
        elif (value - 15) in west:
                player.x_pos = new_x
                maze_walls[new_y][new_x] -= 15

                door_pos = buttons[(new_x, new_y)]
                maze_walls[door_pos[0]][door_pos[1]] -= 30

    if direction == "east":
        new_x += 1
        if new_x < width:
            value = maze_walls[new_y][new_x]

            if (value in north):
                player.x_pos = new_x

            # this is a button that was stepped on
            elif (value - 15) in north:
                player.x_pos = new_x
                maze_walls[new_y][new_x] -= 15

                door_pos = buttons[(new_x, new_y)]
                maze_walls[door_pos[0]][door_pos[1]] -= 30
