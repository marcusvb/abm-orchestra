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


mazeGK = load_map_from_file("concertgebouwmap.txt")


# Define exit point ; garderobe, 6 ingangen

garderobe_1 = Point(23,12)
garderobe_2 = Point(23,23)
garderobe_3 = Point(23,34)
garderobe_4 = Point(23,45)
garderobe_5 = Point(23,57)

# aan de zijkant zaal bij binnekomst
exit_1 = Point(37,6)
exit_2 = Point(81,6)

# aan de zijkant zaal tegenover concertzaal bij binnekomst
exit_3 = Point(37,95)
exit_4 = Point(81,95)

# aan de voorkant van het gebouw

exit_5 = Point(95, 20)
exit_6 = Point(95, 34)
exit_7 = Point(95, 49)

# garderobe exits

exits= [garderobe_1,garderobe_2,garderobe_3,garderobe_4,garderobe_5]

# deur exits

# exits = [exit_1, exit_2, exit_3, exit_4, exit_5, exit_6, exit_7]

directions = direction_map(mazeGK, exits, 1)

# directions = direction_map(mazeGK, exits, 1)


# load the text file

