import glfw
from OpenGL.GL import *
import random
import seaborn as sns
import matplotlib.pyplot as plt

from gfx.MazeTexture import MazeTexture
from model.direction_map.DirectionMap import DirectionMap
from model.environment.line import Point
from gfx.AgentManager import AgentManager
from resources.handling.reading import load_direction_from_file, load_map_from_file
from resources.handling.generatingHeatmap import heatmap_from_map
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

map_filename = "FINAL_MAPS/FINAL_concertgebouwmap.txt" # Seems to be the maze
# map_filename = "concertgebouwmap_advanced.txt" # Seems to be the maze

maze_original = load_map_from_file(map_filename)
maze = load_map_from_file(map_filename)

heatmap = heatmap_from_map(maze)
exit_points = []
for i in range(40, 60):
    exit_points.append(Point(99, i))

# exit_points = []
# for i in range(10, 20):
#     exit_points.append(Point(99, i))
exit_points = None

# directions = direction_map(maze, exit_points, 1) #seems to be the direction map for the agents.
JuulBeaSpiegelChamp = gradient_from_direction_map("FINAL_MAPS/Gradient/JuulBeaSpiegelChamp")
NoordZuid = gradient_from_direction_map("FINAL_MAPS/Gradient/NoordZuid")
GarderobeQ1 = gradient_from_direction_map("FINAL_MAPS/Gradient/Garderobe_Q1")
GarderobeQ2 = gradient_from_direction_map("FINAL_MAPS/Gradient/Garderobe_Q2")
GarderobeQ3 = gradient_from_direction_map("FINAL_MAPS/Gradient/Garderobe_Q3")
GarderobeQ4 = gradient_from_direction_map("FINAL_MAPS/Gradient/Garderobe_Q4")
Trappenhuis_LB = gradient_from_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_LB")
Trappenhuis_LO = gradient_from_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_LO")
Trappenhuis_RB = gradient_from_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_RB")
Trappenhuis_RO = gradient_from_direction_map("FINAL_MAPS/Gradient/TRAPPENHUIS_RO")
DirectUpstairs = gradient_from_direction_map("FINAL_MAPS/Gradient/DirectUpstairs")

garderobes = [GarderobeQ1, GarderobeQ2, GarderobeQ3, GarderobeQ4]

# define type of gradient maps
start_goals = [garderobes[3], DirectUpstairs]
end_goals = [Trappenhuis_RO, Trappenhuis_LB, Trappenhuis_LO, Trappenhuis_RB]
mid_goals = [JuulBeaSpiegelChamp, NoordZuid]


# Config for the window
w_prev = 1280
h_prev = 720

offset = 20

tile_size = [(w_prev - 2 * (offset + 1)) / len(maze[0]), (h_prev - 2 * (offset + 1)) / len(maze)] # agent title size

# Window config end

# Here we give the direction maps to the agent manager
agents = AgentManager(tile_size, w_prev, h_prev, offset, exit_points, maze, start_goals, mid_goals, end_goals, heatmap)
# agents = AgentManager(tile_size, w_prev, h_prev, offset, exit_points, maze, ingangen, heatmap)

mazeTexture = MazeTexture(maze_original, w_prev, h_prev, offset, tile_size)

def plot_heatmap(map):
    sns.heatmap(map, cmap='jet')
    plt.show()

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

        pos = [-1, -1]
        for it in range(len(maze)):
            if tile_size[1] * it < pos_y < tile_size[1] * (it + 1):
                pos[0] = it
        for it in range(len(maze[0])):
            if tile_size[0] * it < pos_x < tile_size[0] * (it + 1):
                pos[1] = it
        if pos[0] != -1 and pos[1] != -1 and maze[pos[0]][pos[1]] != 1:
            agents.add_new(33.0, [.9, .9, .9])


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
agent_colors = [[1.0, 1.0, 1.0],[1.0, 0.5, 0.31], [0.0, 1.0, 0.0]]
agent_color_nr = 0

while not glfw.window_should_close(window):

    current_time = glfw.get_time()

    frame_count += 1

    # change garderobe after 150 frames
    if frame_count % 150 == 0:
        if len(garderobes) > 1:
            del garderobes[-1]
            agents.start_goals = [garderobes[-1], DirectUpstairs]
            agent_color_nr += 1
            agent_color_nr = agent_color_nr % 3

    if simulation_running:
        agents.step()

    if current_time - previous_time >= 1.0:
        title = "Crowd Simulation ( " + str(frame_count) + " FPS | Number Of Agents: " + str(
            len(agents.agent_list)) + " )" + " intensity: " + str(global_intensity)
        glfw.set_window_title(window, title)
        # I commented this so I could use frame_count for changing the garderobe
        # frame_count = 0
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
        agents.add_new(33.0, agent_colors[agent_color_nr])

plot_heatmap(agents.heatmap)

mazeTexture.release()
glfw.terminate()