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

exits = [Point(99,1)]




concertgebouw = load_map_from_file("concertgebouwmap.txt")


# Define exit point ; garderobe, 6 ingangen

garderobe_1 = Point(23,12)
garderobe_2 = Point(23,23)
garderobe_3 = Point(23,34)
garderobe_4 = Point(23,45)
garderobe_5 = Point(23,57)

# aan de zijkant zaal bij binnekomst
zaal_1 = Point(37,6)
zaal_2 = Point(81,6)

# aan de zijkant zaal tegenover concertzaal bij binnekomst
zaal_3 = Point(37,95)
zaal_4 = Point(81,95)

# aan de voorkant van het gebouw

zaal_5 = Point(95, 20)
zaal_6 = Point(95, 34)
zaal_7 = Point(95, 49)

koffiebar_1 = Point(59, 69)
koffiebar_2 = Point(59, 0)

trappenhuis_1 = Point(6,0)
trappenhuis_2 = Point(6,69)

# garderobe exits

garderobe = [garderobe_1,garderobe_2,garderobe_3,garderobe_4,garderobe_5]
zaal = [zaal_1, zaal_2, zaal_3, zaal_4, zaal_5, zaal_6, zaal_7]
koffiebar = [koffiebar_1, koffiebar_2]
trappenhuis = [trappenhuis_1, trappenhuis_2]


# deur exits

# exits = [exit_1, exit_2, exit_3, exit_4, exit_5, exit_6, exit_7]

directionmap_garderobe = direction_map(concertgebouw, garderobe, 1)
directionmap_zaal = direction_map(concertgebouw, zaal, 1)
directionmap_koffiebar =  direction_map(concertgebouw, zaal, 1)



create_txt_form_direction_map("resources/ready/concertgebouw_garderobe.txt", directionmap_garderobe)
create_txt_form_direction_map("resources/ready/", directionmap_zaal)
create_txt_form_direction_map("resources/ready/", directionmap_koffiebar)





mazeGK = load_map_from_file("concertgebouwmap.txt")
print(mazeGK)
directions = direction_map(mazeGK, exits, 1)
create_txt_form_direction_map("ready/small_garderobe2", directions)


# load the text file

