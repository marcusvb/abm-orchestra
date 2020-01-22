import copy

from gfx.AgentGfx import AgentGfx
from model.agent.Agent import ExitReached
import numpy as np


class AgentManager:
    def __init__(self, initial_tile_size: [float, float], client_width: int, client_height: int, map_offset: int,
                 exit, maze, start_goals, direct, end_goals, heatmap):
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
        for agent in self.agent_list:
            agent.draw(self.agent_radius)



    def add_new(self, position, angle: float, color: [float, float, float], which_map = 0):
        all_directions, stairs_garderobe, moving_chance = self.get_specifics()

        correct_pos = [
            0 + self.offset + 1 + (position[1] * self.tile_size[0]) + (self.tile_size[0] / 2),
            self.height - self.offset - 1 - (position[0] * self.tile_size[1]) - (self.tile_size[1] / 2)
        ]

        if self.maze_for_agent[position[0]][position[1]] == 0:
            self.agent_list.append(AgentGfx(correct_pos, position, angle, color, self.maze_for_agent, all_directions, stairs_garderobe))
        else:
            print('Agent can not be added on this pos')

    def step(self):
        moving_lsit = sorted(self.agent_list, key=lambda agt: agt.agent.anger, reverse=True)

        any_moved = True

        while any_moved:
            any_moved = False

            for agent in moving_lsit:
                ag_x, ag_y = agent.agent.current_pos
                self.heatmap[ag_x][ag_y] += 1
                try:
                    anger = agent.move()
                except ExitReached:
                    self.agent_list.remove(agent)
                    moving_lsit.remove(agent)

                else:
                    if anger == 0:
                        any_moved = True
                        moving_lsit.remove(agent)

                        agent.map_position = (ag_x, ag_y)

                        agent.fx_pos = [
                            0 + self.offset + 1 + (agent.map_position[1] * self.tile_size[0]) + (self.tile_size[0] / 2),
                            self.height - self.offset - 1 - (agent.map_position[0] * self.tile_size[1]) - (
                                    self.tile_size[1] / 2)
                        ]

                        agent.position = agent.fx_pos

    def get_specifics(self):

        # decide start position of the agent


        # if np.random.uniform() > 0.675:  # if we're higher we take second entry
        #     start_pos = pos2
        # else:
        #     start_pos = pos1

        # create directions array with specific start and end position
        all_directions = []

        # 5 % will go to the stairs garderobe (start map 1)
        garderobe_choice = np.random.random()
        if garderobe_choice < 0.05:
            all_directions.append(self.start_goals[1])
            stairs_garderobe = 1
        else:
            all_directions.append(self.start_goals[0])
            stairs_garderobe = 0

        all_directions = all_directions + self.direct
        entrance_choice = np.random.choice(len(self.end_goals), 1)
        all_directions.append(self.end_goals[entrance_choice[0]])

        # decide moving chance of the agent with
        # Random postion where our agents start, lower right bottom
        s = np.random.exponential(0.75, 1000)
        s = s * (0.8 / np.amax(s))
        moving_chance = 1 - s

        return all_directions, stairs_garderobe, moving_chance
