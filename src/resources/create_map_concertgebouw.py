from model.environment.environment import direction_map
from model.environment.line import Point
from resources.handling.generating import create_txt_form_direction_map
from resources.handling.reading import load_map_from_file
import numpy as np
from string import digits

# make a numpy array of the concertgebouw

n = 100
maze = [[0 for j in range(0,n)] for i in range(0, 69)]
maze = np.array(maze)
print(maze.shape)



# ONDERSTE EN BOVENSTE OBSTACELS

for x in range(6, 17):
    for y in range(6 , 14):
        maze[y][x] = 1


for x in range(6,17):
    for y in range(55,63):
        maze[y][x] = 1

# MIDDELSTE OBSTACEL

for x in range(6,17):
    for y in range(26,42):
        maze[y][x] = 1

# CONCERTZAAL

for x in range(23,95):
    for y in range(6,63):
        maze[y][x] = 1


# split the maze into 69 horizontal lists

output = np.split(maze, 69)


f = open("concertgebouwmap.txt", "w")
for subarray in output:

    str = np.array_str(subarray)

    tmp = ""

    for d in str:
        try:
            int(d)
            tmp = tmp + d + " "
        except:
            continue
    f.write(tmp + "\n")
    print(tmp)


f.close()

exits = [Point(20,22)]


mazeGK = load_map_from_file("concertgebouwmap.txt")
print(mazeGK)
directions = direction_map(mazeGK, exits, 1)
create_txt_form_direction_map("ready/small_garderobe", directions)

# load the text file

