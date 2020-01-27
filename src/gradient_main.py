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


from model.gradient_agent import MapConfs as MapConf
from model.gradient_agent.RunConf import RunConf

import pandas as pd
import numpy as np


BASE_TITLE = "ABM: Het Concertgebouw Crowd Simulation "

class GradientMain:
    def __init__(self, mapConf):
        self.MapConf = mapConf

    def run(self):
        if not glfw.init():
            exit(1)

        # global_intensity: This dictates how many agents we will spawn somewhere in the simulation.
        # global global_intensity # irrelevant global call

        global_intensity = 50

        window = glfw.create_window(1280, 720, BASE_TITLE, None, None)
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

        # exit_points = []
        # for i in range(10, 20):
        #     exit_points.append(Point(99, i))
        exit_points = None

        # directions = direction_map(maze, exit_points, 1) #seems to be the direction map for the agents.
        JuulBea = gradient_from_direction_map("FINAL_MAPS/Gradient/JuulBea")
        Spiegel = gradient_from_direction_map("FINAL_MAPS/Gradient/Spiegel")
        Champ = gradient_from_direction_map("FINAL_MAPS/Gradient/Champ")
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
        achteringang1 = gradient_from_direction_map("FINAL_MAPS/Gradient/achteringang1")
        achteringang2 = gradient_from_direction_map("FINAL_MAPS/Gradient/achteringang2")
        achteringang3 = gradient_from_direction_map("FINAL_MAPS/Gradient/achteringang3")
        benedeningang1 = gradient_from_direction_map("FINAL_MAPS/Gradient/benedeningang1")
        benedeningang2 = gradient_from_direction_map("FINAL_MAPS/Gradient/benedeningang2")
        boveningang1 = gradient_from_direction_map("FINAL_MAPS/Gradient/boveningang1")
        boveningang2 = gradient_from_direction_map("FINAL_MAPS/Gradient/boveningang2")
        wcman = gradient_from_direction_map("FINAL_MAPS/Gradient/wcman_verbeterd")
        wcvrouw = gradient_from_direction_map("FINAL_MAPS/Gradient/wcvrouw_verbeterd")

        garderobes = [GarderobeQ1, GarderobeQ2, GarderobeQ3, GarderobeQ4]
        torentjes = [Trappenhuis_RO, Trappenhuis_LB, Trappenhuis_LO, Trappenhuis_RB]
        vooringangen = [boveningang1, boveningang2]
        achteringangen = [achteringang1, achteringang2, achteringang3, benedeningang1, benedeningang2]
        zaalingangen = [vooringangen, achteringangen]


        # define type of gradient maps
        start_goals = [garderobes[3], DirectUpstairs]
        mid_goals = [JuulBea, Spiegel, Champ, NoordZuid, wcman, wcvrouw, Trappenhuis_RB, Trappenhuis_RO, Trappenhuis_LO, Trappenhuis_LB]
        end_goals = [torentjes, zaalingangen]



        # Config for the window
        w_prev = 1280
        h_prev = 720

        offset = 20

        tile_size = [(w_prev - 2 * (offset + 1)) / len(maze[0]), (h_prev - 2 * (offset + 1)) / len(maze)] # agent title size


        # Window config end

        # Here we give the direction maps to the agent manager
        agents = AgentManager(tile_size, w_prev, h_prev, offset, exit_points, maze, start_goals, mid_goals, end_goals, heatmap, MapConf)

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

                    # add agent at entrance 1
                    agents.add_new([139, np.random.randint(83, 89)], 33.0, [.9, .9, .9], frame_count)


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

        if self.MapConf.RunTime.VISUALIZE:
            glfw.set_mouse_button_callback(window, mouse_button_callback)
            glfw.set_key_callback(window, key_callback)

        old_step_time = glfw.get_time()
        previous_time = glfw.get_time()

        # variables for the quarter updates
        frame_count = 0
        agent_colors = [[1.0, 1.0, 1.0], [1.0, 0.5, 0.31], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        zuid_2_probabilities = [self.MapConf.RunTime.Z2_Q1, self.MapConf.RunTime.Z2_Q2, self.MapConf.RunTime.Z2_Q3, self.MapConf.RunTime.Z2_Q4]
        zuid_1_probabilities = [self.MapConf.RunTime.Z1_Q1, self.MapConf.RunTime.Z1_Q2, self.MapConf.RunTime.Z1_Q3, self.MapConf.RunTime.Z1_Q4]
        agent_color_nr = 0
        entrance_1_probability = zuid_2_probabilities[0]
        entrance_2_probability = zuid_1_probabilities[0]

        while not glfw.window_should_close(window):

            current_time = glfw.get_time()

            frame_count += 1

            # next quarter changes
            if frame_count % (self.MapConf.RunTime.MAX_FRAMES / 4) == 0:

                agents.flowvalidation_update()
                agents.density_count()

                # if statement can be removed when quarter is 2000 and runtime is 8000
                if len(garderobes) > 1:
                    del garderobes[-1]
                    agents.start_goals = [garderobes[-1], DirectUpstairs]
                    agent_color_nr += 1
                    agent_color_nr = agent_color_nr % 3

                    del zuid_1_probabilities[0]
                    del zuid_2_probabilities[0]
                    entrance_2_probability = zuid_1_probabilities[0]
                    entrance_1_probability = zuid_2_probabilities[0]

            if simulation_running:
                agents.step()

            if current_time - previous_time >= 1.0:
                title = BASE_TITLE + " ( FRAME COUNT: " + str(frame_count) + " | Number Of Agents: " + str(
                    len(agents.agent_list)) + " )" + " intensity: " + str(global_intensity)
                glfw.set_window_title(window, title)

                # If we don't opengl visualization we print the sim status to stdout
                if not self.MapConf.RunTime.VISUALIZE:
                    print(title)

                # I commented this so I could use frame_count for changing the garderobe
                # frame_count = 0
                previous_time = current_time

            if self.MapConf.RunTime.VISUALIZE:
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

            # intensity = random.randint(0, 100)
            # if intensity < global_intensity:
            #     agents.add_new(33.0, agent_colors[agent_color_nr])

            entrance1 = [139, np.random.randint(83, 89)]  # ZUID 2 INGANG
            entrance2 = [139, np.random.randint(162, 168)]  # ZUID 1 INGANG
            entrance_1_rv = random.random()

            if entrance_1_rv < entrance_1_probability:
                agents.add_new(entrance1, 33.0, agent_colors[agent_color_nr], frame_count)
                agents.add_new(entrance1, 33.0, agent_colors[agent_color_nr], frame_count)

            entrance_2_rv = random.random()
            if entrance_2_rv < entrance_2_probability:
                agents.add_new(entrance2, 33.0, agent_colors[agent_color_nr], frame_count)

            #  Set the window to close terminate the outer whileloop
            if frame_count > self.MapConf.RunTime.FINAL_STOP_FRAME/4:

                csv_Dataframe = pd.DataFrame([agents.zuidValidationCountList, agents.noordValidationCountList,
                                              agents.champagneValidationCountList, agents.noordDensity,
                                              agents.zuidDensity, agents.gardiDensity])
                csv_Dataframe = np.transpose(csv_Dataframe)

                csv_Dataframe.to_csv(r'Logs/SA_data.txt', header=None, index=None, sep=',', mode='a')

                glfw.set_window_should_close(window, True)

        # Validation_dataframe = pd.DataFrame([agents.zuidValidationCountList, agents.noordValidationCountList, agents.champagneValidationCountList])
        # Validation_dataframe=np.transpose(Validation_dataframe)
        # Validation_dataframe.columns = ['Validation Zuid', 'Validation Noord', 'Validation Champagne']
        #
        # Density_dataframe = pd.DataFrame([agents.noordDensity, agents.zuidDensity, agents.gardiDensity])
        # Density_dataframe=np.transpose(Density_dataframe)
        # Density_dataframe.columns =['Density Zuid', 'Density Noord', 'Density Garderobe']

        # mazeTexture.release()
        glfw.terminate()
        plot_heatmap(agents.heatmap)


