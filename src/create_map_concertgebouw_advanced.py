import os, sys

from model.environment.environment import direction_map
from model.environment.line import Point
from resources.handling.generating import create_txt_form_direction_map
from resources.handling.reading import load_map_from_file
import numpy as np
from string import digits

# make a numpy array of the concertgebouw ground floor

n = 200
maze = [[1 for j in range(0,n)] for i in range(0, n)]   #generate 200x200 grid of obstacle material
maze = np.array(maze)
print(maze.shape)

#BEA, JULIANA

for x in range(30, 62):            #Juliana(31x16)
    for y in range(57 , 73):
        maze[y][x] = 0

for x in range(30, 62):             #Bea(31x16)
    for y in range(125, 141):
        maze[y][x] = 0


for width in range(5):      #corridors to the spiegelzaal
    for k in range(10):
        maze[125-k][40-k+width] = 0
        maze[73+k][40-k+width] = 0


#SPIEGELZAAL
for x in range(10, 46):   #middle of y-axis
    for y in range(89, 109):
        maze[y][x] = 0

for x in range(22, 34):  #middle of x-axis
    for y in range(75, 123):
        maze[y][x] = 0

#First two x steps, take double step in y direction
for x in range(11,45):
    for y in range(87, 111):
        maze[y][x] = 0

for x in range(12,44):
    for y in range(85, 113):
        maze[y][x] = 0

#Take step in x and step in y direction
for k in range(10):
    for x in range(13+k, 43-k):
        for y in range(85-k, 113+k):
            maze[y][x] = 0

#Hall towards Cloakroom
for x in range(46,63):
    for y in range(95, 103):
        maze[y][x] = 0

#WC's
for x in range(49,62):
    for y in range(75,93):
        maze[y][x] = 0
    for y in range(105,123):
        maze[y][x] = 0

# DEUREN VANAF LINKERDEEL NAAR RECHTERDEEL

for y in range(57,63):
    maze[y][62] = 0
for y in range(135,141):
    maze[y][62] = 0
for y in range(87,90):
    maze[y][62] = 0
for y in range(115, 118):
    maze[y][62] = 0

# Entire hall
for x in range(63,185):
    for y in range(57,141):
        maze[y][x] = 0

# ONDERSTE EN BOVENSTE OBSTAKELS

for x in range(69,81):
    for y in range(64,74):
        maze[y][x] = 1

for x in range(69,81):
    for y in range(124,134):
        maze[y][x] = 1

# MIDDELSTE OBSTAKEL

for x in range(69,81):
    for y in range(89,108):
        maze[y][x] = 1

for x in range(70,80):
    for y in range(90,107):
        maze[y][x] = 0

for x in range(72,75):
    maze[89][x] = 0


# CONCERTZAAL

for x in range(90,177):
    for y in range(64,134):
        maze[y][x] = 1

# ZUID (48x12)

for x in range(95, 144):
    for y in range(44, 57):
        maze[y][x] = 0

# NOORD

for x in range(101, 149):
    for y in range(141, 154):
        maze[y][x] = 0

# CHAMPAGNE

for x in range(185,196):
    for y in range(85,113):
        maze[y][x] = 0


# split the maze into 200 horizontal lists

output = np.split(maze, 200)


f = open("concertgebouwmap_advanced.txt", "w")
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

# exits = [Point(20,22)]
#
#
# mazeGK = load_map_from_file("concertgebouwmap_advanced.txt")
# print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("resources/ready/CG_ADVANCED_TRIAL.txt", directions)

# load the text file

