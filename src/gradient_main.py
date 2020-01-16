import glfw
from OpenGL.GL import *
import random

from gfx.MazeTexture import MazeTexture
from model.direction_map.DirectionMap import DirectionMap
from model.environment.line import Point
from gfx.AgentManager import AgentManager
from resources.handling.reading import load_direction_from_file, load_map_from_file
from model.gradient.gradient_map import gradient_from_direction_map

import numpy as np

if not glfw.init():
    exit(1)

# global_intensity: This dictates how many agents we will spawn somewhere in the simulation.
# global global_intensity # irrelevant global call

global_intensity = 50

window = glfw.create_window(1280, 720, "Here comes out project title.", None, None)
glfw.make_context_current(window)

simulation_running = True

if not window:
    glfw.terminate()
    exit(1)

map_filename = "resources/ready/concertgebouwmap.txt" # Seems to be the maze

maze_original = load_map_from_file(map_filename)
maze = load_map_from_file(map_filename)

# exit points are generated here. Not sure how the gradient based model makes the agents use the exit points.
# I think this param is probably used for the on-the-fly gradient based simulation. For now going to None before refactor.

# exit_points = []
# for i in range(10, 20):
#     exit_points.append(Point(99, i))
exit_points = None

# directions = direction_map(maze, exit_points, 1) #seems to be the direction map for the agents.
direction1 = gradient_from_direction_map("resources/ready/concertgebouw_direction_100x100.txt")
# direction2 = gradient_from_direction_map("resources/ready/GK_directionmap_two_100x100.txt")
# direction3 = gradient_from_direction_map("resources/ready/GK_directionmap_three_100x100.txt")
# direction4 = gradient_from_direction_map("resources/ready/GK_directionmap_four_100x100.txt")

direct = [direction1]

# Config for the window
w_prev = 1280
h_prev = 720

offset = 20

tile_size = [(w_prev - 2 * (offset + 1)) / len(maze[0]), (h_prev - 2 * (offset + 1)) / len(maze)] # agent title size

# Window config end

agents = AgentManager(tile_size, w_prev, h_prev, offset, exit_points, maze, direct)

mazeTexture = MazeTexture(maze_original, w_prev, h_prev, offset, tile_size)


"""
Model control via IO.
This should actually go to a separate handler in folder, and then cleanup missing references
to global variables etc. etc. 
"""
def mouse_button_callback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        pos_x, pos_y = glfw.get_cursor_pos(window)
        pos_x -= offset
        pos_y -= offset

        print("x, y", pos_x, pos_y)

        pos = [-1, -1]
        for it in range(len(maze)):
            if tile_size[1] * it < pos_y < tile_size[1] * (it + 1):
                pos[0] = it
        for it in range(len(maze[0])):
            if tile_size[0] * it < pos_x < tile_size[0] * (it + 1):
                pos[1] = it
        if pos[0] != -1 and pos[1] != -1 and maze[pos[0]][pos[1]] != 1:
            agents.add_new(pos, 33.0, [.0, .0, .9], 0)


def key_callback(window, key, scancode, action, mods):
    global global_intensity
    if key == glfw.KEY_KP_ADD and action == glfw.RELEASE:
        global_intensity += 10
        if global_intensity > 100:
            global_intensity = 100
    if key == glfw.KEY_KP_SUBTRACT and action == glfw.RELEASE:
        global_intensity -= 10
        if global_intensity < 0:
            global_intensity = 0
    if key == glfw.KEY_KP_ADD and action == glfw.RELEASE:
        print("Wcisnalem!")
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        global simulation_running
        simulation_running = not (simulation_running and True)


glfw.set_mouse_button_callback(window, mouse_button_callback)
glfw.set_key_callback(window, key_callback)

old_step_time = glfw.get_time()
previous_time = glfw.get_time()
frame_count = 0

while not glfw.window_should_close(window):

    current_time = glfw.get_time()
    frame_count += 1

    if simulation_running:
        agents.step()

    if current_time - previous_time >= 1.0:
        title = "Crowd Simulation ( " + str(frame_count) + " FPS | Number Of Agents: " + str(
            len(agents.agent_list)) + " )" + " intensity: " + str(global_intensity)
        glfw.set_window_title(window, title)
        frame_count = 0
        previous_time = current_time

    glfw.poll_events()

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    w, h = glfw.get_window_size(window)

    if w != w_prev or h != h_prev:
        w_prev = w
        h_prev = h
        tile_size[0] = (w - 2 * (offset + 1)) / len(maze[0])
        tile_size[1] = (h - 2 * (offset + 1)) / len(maze)
        agents.set_client_tile_size(w, h, tile_size)
        mazeTexture.reconstruct(w, h, tile_size)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, 0, h, -10, 10)

    glMatrixMode(GL_MODELVIEW)

    mazeTexture.draw()

    agents.draw_all()

    glfw.swap_buffers(window)

    intensity = random.randint(0, 100)
    if intensity < global_intensity:


        # Random postion where out agents start, lower right bottom
        pos = [68, random.randint(16, 22)] # ZUID 2 INGANG
        pos2 = [68, random.randint(77, 83)] # ZUID 1 INGANG


        if np.random.uniform() > 0.675 : #if we're higher we take second entry
            pos = pos2

        "Here we add agents randomly uniform between either map 0 and 1"
        agents.add_new(pos, 33.0, [.0, .0, .9], 0)

        "Here we add agents randomly uniform between either map 0 and 1"
        # pos = [randint(2, 90), 2]
        # which_map = randint(2, 3)
        # agents.add_new(pos, 33.0, [.0, .0, .9], which_map)

mazeTexture.release()
glfw.terminate()