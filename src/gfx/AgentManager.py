import copy

from gfx.AgentGfx import AgentGfx
from model.agent.Agent import ExitReached
import numpy as np
import pandas as pd
from scipy import stats

from model.gradient_agent.RunConf import RunConf


class AgentManager:
    def __init__(self, initial_tile_size: [float, float], client_width: int, client_height: int, map_offset: int,
                 exit, maze, start_goals, direct, end_goals, heatmap, MapConf):
        self.agent_list = list()
        self.tile_size = initial_tile_size
        self.agent_radius = (initial_tile_size[1] - initial_tile_size[1] / 5) / 2
        self.width = client_width
        self.height = client_height
        self.offset = map_offset
        self.exit_points = exit
        self.maze = maze
        self.maze_for_agent=copy.deepcopy(maze)
        self.direct = direct
        self.heatmap = heatmap
        self.start_goals = start_goals
        self.end_goals = end_goals
        self.MapConf = MapConf

        self.zuidValidationCount = 0
        self.noordValidationCount = 0
        self.champagneValidationCount = 0

        self.zuidValidationCountList = []
        self.noordValidationCountList = []
        self.champagneValidationCountList = []

        self.noordDensity = []
        self.zuidDensity = []
        self.gardiDensity = []

    def set_client_tile_size(self, client_width: int, client_height: int, tile_size: [float, float]):
        self.width = client_width
        self.height = client_height
        self.tile_size = tile_size
        self.agent_radius = (tile_size[1] - tile_size[1] / 5) / 2

        for agent in self.agent_list:
            correct_pos = [
                0 + self.offset + 1 + (agent.map_position[1] * self.tile_size[0]) + (self.tile_size[0] / 2),
                self.height - self.offset - 1 - (agent.map_position[0] * self.tile_size[1]) - (self.tile_size[1] / 2)
            ]
            agent.position = correct_pos

    def draw_all(self):
        dijkstra_count = 0
        count = 0
        for agent in self.agent_list:
            conf = agent.draw(self.agent_radius)
            if conf == RunConf.DIJKSTRA:
                dijkstra_count += 1
            count += 1

        # if count:
            # print("This frame", np.round(dijkstra_count/count, 2) * 100, "% were dijkstra")

    def density_count(self):

        xmin_Noord = 100
        xmax_Noord = 149
        ymin_Noord = 44
        ymax_Noord = 64

        Noord = 0

        for ag in self.agent_list:
            ag_y, ag_x = ag.agent.current_pos
            if ag_x > xmin_Noord and ag_x < xmax_Noord and ag_y > ymin_Noord and ag_y < ymax_Noord:
                Noord += 1
        self.noordDensity.append(Noord)

        xmin_Zuid = 94
        xmax_Zuid = 144
        ymin_Zuid = 133
        ymax_Zuid = 154

        Zuid = 0

        for ag in self.agent_list:
            ag_y, ag_x = ag.agent.current_pos
            if ag_x > xmin_Zuid and ag_x < xmax_Zuid and ag_y > ymin_Zuid and ag_y < ymax_Zuid:
                Zuid += 1
        self.zuidDensity.append(Zuid)

        xmin_Gard = 81
        xmax_Gard = 90
        ymin_Gard = 88
        ymax_Gard = 108

        Garderobe = 0

        for ag in self.agent_list:
            ag_y, ag_x = ag.agent.current_pos
            if ag_x > xmin_Gard and ag_x < xmax_Gard and ag_y > ymin_Gard and ag_y < ymax_Gard:
                Garderobe += 1
        self.gardiDensity.append(Garderobe)

    def add_new(self, position, angle: float, color: [float, float, float], current_frame):
        all_directions, stairs_garderobe, moving_chance, end_goal_frame = self.get_specifics(current_frame)

        correct_pos = [
            0 + self.offset + 1 + (position[1] * self.tile_size[0]) + (self.tile_size[0] / 2),
            self.height - self.offset - 1 - (position[0] * self.tile_size[1]) - (self.tile_size[1] / 2)
        ]

        if self.maze_for_agent[position[0]][position[1]] == 0:
            self.agent_list.append(AgentGfx(correct_pos, position, angle, color, self.maze_for_agent, all_directions, stairs_garderobe, end_goal_frame, current_frame, moving_chance, self.MapConf))
        else:
            pass
            # print('Agent can not be added on this pos')

    def flowvalidation_update(self):
        self.zuidValidationCountList.append(self.zuidValidationCount)
        self.noordValidationCountList.append(self.noordValidationCount)
        self.champagneValidationCountList.append(self.champagneValidationCount)

        self.zuidValidationCount = 0
        self.noordValidationCount = 0
        self.champagneValidationCount = 0


    def validate_step(self, ag_x, ag_y):

        if ag_x == 94 and ag_y < 141 and ag_y > 133:
            self.zuidValidationCount += 1

        elif ag_x == 89 and ag_y < 64 and ag_y > 57:
            self.noordValidationCount += 1

        elif ag_x > 176 and ag_x < 185 and ag_y == 84:
            self.champagneValidationCount += 1


    def step(self):
        moving_lsit = sorted(self.agent_list, key=lambda agt: agt.agent.anger, reverse=True)

        any_moved = True

        while any_moved:
            any_moved = False

            for agent in moving_lsit:
                ag_y, ag_x = agent.agent.current_pos

                self.validate_step(ag_x, ag_y)

                #DO NOT ADD COFFEE DRINKING AGENTS INTO HEATMAP
                if agent.agent.moving_random == False or agent.agent.waitingongarderobe == False or agent.agent.sitting_on_toilet == False:
                    self.heatmap[ag_y][ag_x] += 1


                try:
                    anger = agent.move()
                except ExitReached:
                    self.agent_list.remove(agent)
                    moving_lsit.remove(agent)

                else:
                    if anger == 0:
                        any_moved = True
                        moving_lsit.remove(agent)

                        agent.map_position = (ag_y, ag_x)

                        agent.fx_pos = [
                            0 + self.offset + 1 + (agent.map_position[1] * self.tile_size[0]) + (self.tile_size[0] / 2),
                            self.height - self.offset - 1 - (agent.map_position[0] * self.tile_size[1]) - (
                                    self.tile_size[1] / 2)
                        ]

                        agent.position = agent.fx_pos

    def get_specifics(self, current_frame):
        all_directions = []

        # 5 % will go to the stairs garderobe (start map 1)
        garderobe_choice = np.random.random()
        if garderobe_choice < self.MapConf.Chances.STAIRS_GARDEROBE:
            all_directions.append(self.start_goals[1])
            stairs_garderobe = 1
        else:
            all_directions.append(self.start_goals[0])
            stairs_garderobe = 0

        all_directions = all_directions + self.direct

        entrance_choice = np.random.random()
        if entrance_choice < self.MapConf.Chances.TORENTJE:
            # torentje entrances
            entrances = self.end_goals[0]
        else:
            # zaal entrances, 1/3 achteringang
            entrance_choice = np.random.random()
            if entrance_choice < self.MapConf.Chances.BACK_ENTRANCE:

                # achteringang entrances
                entrances = self.end_goals[1][1]
            else:

                # vooringang entrances
                entrances = self.end_goals[1][0]

        # choose random from selected entrance options
        entrance_choosing = np.random.choice(len(entrances), 1)
        entrance = entrances[entrance_choosing[0]]

        # add to direction as final entrance
        all_directions.append(entrance)

        # decide moving chance of the agent, now everyone the same always walking
        moving_chance = 1

        end_goal_frame = self.scaleDistribution(current_frame - 1, self.MapConf.RunTime.MAX_FRAMES)

        return all_directions, stairs_garderobe, moving_chance, end_goal_frame


    def scaleDistribution(self, CurrentFrame, MaxFrame):
        # If Agent enters building in the last quarter, he is in a hurry. So we sample from normal distribution
        if CurrentFrame > 0.75 * MaxFrame:
            try:
                sample = int((CurrentFrame + MaxFrame) / 2 + np.random.normal(0, (MaxFrame - CurrentFrame) / 10, 1))
            except:
                return CurrentFrame
            return sample

        # Else we sample from a skewed normal distribution, so there is a larger chance that agent enters in the last quarter
        else:
            a, loc, scale = 15, 0.1, 1  # Sample from a Skewed Normal Distribution
            sample = stats.skewnorm(a, loc, scale).rvs(1)[0]
            scaler = 4   #max of 10000 samples from the skewednormal lies around 4
            sampleScaled = int(MaxFrame - (MaxFrame - CurrentFrame) * sample / scaler)

            return sampleScaled