import glfw
from OpenGL.GL import *
import random
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

import pickle

from gfx.MazeTexture import MazeTexture
from model.direction_map.DirectionMap import DirectionMap
from model.environment.line import Point
from gfx.AgentManager import AgentManager
from resources.handling.reading import load_direction_from_file, load_map_from_file
from resources.handling.generatingHeatmap import heatmap_from_map
from model.gradient.gradient_map import gradient_from_direction_map
from model.gradient_agent import MapConfs as MapConf

import pandas as pd
import numpy as np


BASE_TITLE = "ABM: Het Concertgebouw Crowd Simulation "

class GradientMain:
    def __init__(self, mapConf):
        self.MapConf = mapConf

    def load_Direct_upstairs_entrance(self, new_entrance):
        if new_entrance:
            return gradient_from_direction_map("FINAL_MAPS/Gradient/DirectUpstairsNoordEntrance")
        return gradient_from_direction_map("FINAL_MAPS/Gradient/DirectUpstairs")

    def load_entrance_2_chances(self, new_entrance):
        if new_entrance:
            return [57, np.random.randint(162, 168)]
        return [139, np.random.randint(162, 168)]


    def run(self, sema=None, lock=None, id=0, new_entrance=False):
        if not glfw.init():
            exit(1)

        self.id = id

        window = glfw.create_window(1280, 720, BASE_TITLE, None, None)
        glfw.make_context_current(window)

        simulation_running = True

        if not window:
            glfw.terminate()
            exit(1)

        map_filename = "FINAL_MAPS/FINAL_concertgebouwmap.txt" # Seems to be the maze

        maze_original = load_map_from_file(map_filename)
        maze = load_map_from_file(map_filename)

        heatmap = heatmap_from_map(maze)
        validationlist = []

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
        DirectUpstairs = self.load_Direct_upstairs_entrance(new_entrance)
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
            plt.figure(dpi=300)
            sns.heatmap(map, cmap='jet')
            plt.show()


        def count_crowded_area_spots(map):
            measure = 0
            for row in map[57:140]:
                for point in row[81:90]:
                    measure += point

            return point

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

                #FOR VALIDATION ONLY TAKE THE VALUES IN ZUID AND APPEND TO VALIDATIONLIST

                agents.density_count()
                # validationlist.append([agents.zuidValidationCount, agents.zuidDensity])
                # agents.flowvalidation_reset()

                # Use lock to mitigate datarace

                validation_Dataframe = pd.DataFrame([self.id, frame_count, agents.zuidValidationCount, agents.zuidDensity])
                np.transpose(validation_Dataframe)

                if lock:
                    lock.acquire()
                    validation_Dataframe.to_csv(r'Logs/Validation_output.txt', header=None, index=None, sep=',', mode='a')
                    lock.release()
                else:
                    validation_Dataframe.to_csv(r'Logs/Validation_output.txt', header=None, index=None, sep=',', mode='a')


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
                title = "ID: " + str(id) + " :: " + BASE_TITLE + " ( FRAME COUNT: " + str(frame_count) + " | Number Of Agents: " + str(len(agents.agent_list)) + " ) NEW ENTRANCE: " + str(new_entrance)
                glfw.set_window_title(window, title)

                # If we don't opengl visualization we print the sim status to stdout
                if not self.MapConf.RunTime.VISUALIZE:
                    if frame_count % 20 == 0:
                        print(title)

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

                """
                Dump OpenGL Buffer to png file for film making!
                """
                if frame_count > 1 and self.MapConf.RunTime.RECORD_VIS:
                    x, y = 0, 0
                    w, h = 2484, 1364 # MARCUS Macbook res, (possible retina upscaling) ?
                    # w, h = 1280, 720 # Normal
                    data = glReadPixels(x, y, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
                    image = Image.frombytes("RGBA", (w, h), data)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                    image.save("images/pic" + str(frame_count).zfill(4) + ".png")

            entrance1_1 = [139, np.random.randint(83, 89)]  # ZUID 2 INGANG
            entrance1_2 = [139, np.random.randint(83, 89)]  # ZUID 2 INGANG

            entrance2 = self.load_entrance_2_chances(new_entrance)  # Chances for North or South entrance
            entrance_1_rv = random.random()

            if frame_count < self.MapConf.RunTime.MAX_FRAMES:
                if entrance_1_rv < entrance_1_probability:
                    agents.add_new(entrance1_1, 33.0, agent_colors[agent_color_nr], frame_count)
                    agents.add_new(entrance1_2, 33.0, agent_colors[agent_color_nr], frame_count)

                entrance_2_rv = random.random()
                if entrance_2_rv < entrance_2_probability:
                    agents.add_new(entrance2, 33.0, agent_colors[agent_color_nr], frame_count)

            #  Set the window to close terminate the outer whileloop
            if frame_count > self.MapConf.RunTime.FINAL_STOP_FRAME:
                glfw.set_window_should_close(window, True)




                # agents.density_count()
                # csv_Dataframe = pd.DataFrame([agents.zuidValidationCount, agents.noordValidationCount,
                #                               agents.champagneValidationCount, agents.noordDensity,
                #                               agents.zuidDensity, agents.gardiDensity])
                # csv_Dataframe = np.transpose(csv_Dataframe)
                # # Use lock to mitigate datarace
                # if lock:
                #     lock.acquire()
                #     # Prepend the ID to the array for ordering later
                #     csv_Dataframe.insert(0, "id", id)
                #     csv_Dataframe.to_csv(r'Logs/SA_data.txt', header=None, index=None, sep=',', mode='a')
                #     lock.release()

        # Append heatmap data in pickle format
        with open(r'Logs/Heatmap_pickle', 'ab') as filepick:
            if lock:
                lock.acquire()
                pickle.dump(agents.heatmap, filepick)
                lock.release()
            else:
                pickle.dump(agents.heatmap, filepick)


        # validation_Dataframe = pd.DataFrame([validationlist])
        # lock.acquire()
        # validation_Dataframe.to_csv(r'Logs/Validation_output.txt', header=None, index=None, sep=',', mode='a')
        # lock.release()


        # Validation_dat/aframe = pd.DataFrame([agents.zuidValidationCountList, agents.noordValidationCountList, agents.champagneValidationCountList])
        # Validation_dataframe=np.transpose(Validation_dataframe)
        # Validation_dataframe.columns = ['Validation Zuid', 'Validation Noord', 'Validation Champagne']
        #
        # Density_dataframe = pd.DataFrame([agents.noordDensity, agents.zuidDensity, agents.gardiDensity])
        # Density_dataframe=np.transpose(Density_dataframe)
        # Density_dataframe.columns =['Density Zuid', 'Density Noord', 'Density Garderobe']

        # mazeTexture.release()
        glfw.terminate()
        # plot_heatmap(agents.heatmap)
        # with open(r'Logs/Heatmap_pickle', 'wb') as fp:
        #     pickle.dump(agents.heatmap, fp)
        if sema:
            sema.release()

        return 0

# x = pd.read_csv(r'Logs/Validation_output.txt')
# x.columns = ['Q1', 'Q2', 'Q3', 'Q4']