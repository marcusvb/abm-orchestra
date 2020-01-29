import os, sys

from model.environment.environment import direction_map
from model.environment.line import Point
from resources.handling.generating import create_txt_form_direction_map
from resources.handling.reading import load_map_from_file
import numpy as np

import time


from string import digits

# make a numpy array of the concertgebouw ground floor

# n = 200
# maze = [[1 for j in range(0,n)] for i in range(0, n)]   #generate 200x200 grid of obstacle material
# maze = np.array(maze)
# print(maze.shape)
#
# #BEA, JULIANA
#
# for x in range(30, 62):            #Juliana(31x16)
#     for y in range(57 , 73):
#         maze[y][x] = 0
#
# for x in range(30, 62):             #Bea(31x16)
#     for y in range(125, 141):
#         maze[y][x] = 0
#
# for width in range(5):      #corridors to the spiegelzaal
#     for k in range(10):
#         maze[125-k][40-k+width] = 0
#         maze[73+k][40-k+width] = 0
#
# #SPIEGELZAAL
# for x in range(10, 46):   #middle of y-axis
#     for y in range(89, 109):
#         maze[y][x] = 0
#
# for x in range(22, 34):  #middle of x-axis
#     for y in range(75, 123):
#         maze[y][x] = 0
#
# #First two x steps, take double step in y direction
# for x in range(11,45):
#     for y in range(87, 111):
#         maze[y][x] = 0
#
# for x in range(12,44):
#     for y in range(85, 113):
#         maze[y][x] = 0
#
# #Take step in x and step in y direction
# for k in range(10):
#     for x in range(13+k, 43-k):
#         for y in range(85-k, 113+k):
#             maze[y][x] = 0
#
# #Hall towards Cloakroom
# for x in range(46,63):
#     for y in range(95, 103):
#         maze[y][x] = 0
#
# #WC's
# for x in range(49,62):
#     for y in range(75,93):
#         maze[y][x] = 0
#     for y in range(105,123):
#         maze[y][x] = 0
#
# # DEUREN VANAF LINKERDEEL NAAR RECHTERDEEL
#
# for y in range(57,63):
#     maze[y][62] = 0
# for y in range(135,141):
#     maze[y][62] = 0
# for y in range(87,90):
#     maze[y][62] = 0
# for y in range(115, 118):
#     maze[y][62] = 0
#
# # Entire hall
# for x in range(63,185):
#     for y in range(57,141):
#         maze[y][x] = 0
#
# # ONDERSTE EN BOVENSTE OBSTAKELS
#
# for x in range(69,81):
#     for y in range(64,74):
#         maze[y][x] = 1
#
# for x in range(69,81):
#     for y in range(124,134):
#         maze[y][x] = 1
#
# # MIDDELSTE OBSTAKEL
#
# for x in range(69,81):
#     for y in range(89,108):
#         maze[y][x] = 1
#
# for x in range(70,80):
#     for y in range(90,107):
#         maze[y][x] = 0
#
# for x in range(72,75):
#     maze[89][x] = 0
#
#
# # CONCERTZAAL
#
# for x in range(90,177):
#     for y in range(64,134):
#         maze[y][x] = 1
#
# # ZUID (48x12)
#
# for x in range(95, 144):
#     for y in range(141, 154):
#         maze[y][x] = 0
#
# # NOORD
#
# for x in range(101, 149):
#     for y in range(44, 57):
#         maze[y][x] = 0
#
# # CHAMPAGNE
#
# for x in range(185,196):
#     for y in range(85,113):
#         maze[y][x] = 0
#
#
# # split the maze into 200 horizontal lists
#
# output = np.split(maze, 200)
#
# f = open("FINAL_MAPS/FINAL_concertgebouwmap.txt", "w")
# for subarray in output:
#
#     str = np.array_str(subarray)
#
#     tmp = ""
#
#     for d in str:
#         try:
#             int(d)
#             tmp = tmp + d + " "
#         except:
#             continue
#     f.write(tmp + "\n")
#     print(tmp)
#
#
# f.close()

# start = time.time()
#
# exits = []
# for i,pos in enumerate([(35, 60),(50, 60),(35, 137),(50, 137)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/JuulBea", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
#
#
#
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(14, 93),(14,104)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/Spiegel", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
#
#
#
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(188,109)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/Champ", directions)
# # load the text file
#
# end = time.time()
# print(end - start)








#
#
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(106,149),(109,149),(128,149),(131,149),(115,47),(112,47),(134,47),(137,47)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/NoordZuid", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
# # NOORD = (115,47),(112,47),(134,47),(137,47),
# # ZUID = (106,149),(109,149),(128,149),(131,149),




# start = time.time()
#
#
# exits = []
# for i,pos in enumerate([(89,68),(89,74),(89,80),(89,86),(89,92)]):
#     print(i)
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/Garderobe_Q4", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
# #

#
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(89,80),(89,86),(89,92),(89,98),(89,104)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/Garderobe_Q3", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(89,92),(89,98),(89,104),(89,110),(89,116)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/Garderobe_Q2", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
# start = time.time()
#
#
# exits = []
# for i,pos in enumerate([(89,104),(89,110),(89,116),(89,122),(89,128)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/Garderobe_Q1", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
# start = time.time()
#
#
# exits = []
# for i,pos in enumerate([(69,140)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_LO", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
# exits = []
# for i,pos in enumerate([(177,140)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_RO", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
# exits = []
# for i,pos in enumerate([(69,57)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_LB", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
exits = []
for i,pos in enumerate([(69,140), (177,57)]):
    exits.append(Point(pos[0],pos[1]))
mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
#print(mazeGK)
directions = direction_map(mazeGK, exits, 1)
create_txt_form_direction_map("FINAL_MAPS/Gradient/DirectUpstairsNoordEntrance", directions)
#
# # load the text file
#
#
#
# exits = []
# for i,pos in enumerate([(177,57)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_RB", directions)
# # load the text file
#
#
#
#
# exits = []
# for i,pos in enumerate([(177,79)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/achteringang1", directions)
# # load the text file
#
#
# start = time.time()
#
#
# exits = []
# for i,pos in enumerate([(177,99)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/achteringang2", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
#
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(177,119)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/achteringang3", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(102,63)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/benedeningang1", directions)
# # load the text file
# end = time.time()
# print(end - start)
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(160,63)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/benedeningang2", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(102,134)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/boveningang1", directions)
# # load the text file
#
# end = time.time()
# print(end - start)
# start = time.time()
#
# exits = []
# for i,pos in enumerate([(160,134)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/boveningang2", directions)
# # load the text file
#
# end = time.time()
# print(end - start)


#
# start = time.time()
# exits = []
# for i,pos in enumerate([(50,108),(50,111),(50,114),(50,117),(50,120),(78,92),(78,98),(78,104)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/wcvrouw_verbeterd", directions)
# # load the text file
#
#
# end = time.time()
# print(end - start)
# start = time.time()
#
#
# exits = []
# for i,pos in enumerate([(50,77),(50,80),(50,83),(50,86),(50,89)]):
#     exits.append(Point(pos[0],pos[1]))
# mazeGK = load_map_from_file("FINAL_MAPS/FINAL_concertgebouwmap.txt")
# # print(mazeGK)
# directions = direction_map(mazeGK, exits, 1)
# create_txt_form_direction_map("FINAL_MAPS/Gradient/wcman_verbeterd", directions)
# # load the text file
#
# end = time.time()
# print(end - start)