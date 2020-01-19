from copy import deepcopy
from random import randint
import numpy as np

import model.navigator.navigator as nav
import model.graph.translation as trans
from model.agent.Agent import ExitReached
from model.environment.environment_enum import Env


class Agent:
    id = 0

    def __init__(self, start_position: (int, int), end_position: [(int, int)], gradient_maps,
                 collision_map: [[(int, int)]], which_gradient_map=0, bound_size=2):
        self.start = start_position
        self.end = end_position
        self.current_pos = self.start
        self.front_collision_size = bound_size
        self.direction_map = gradient_maps[which_gradient_map]
        self.collision_map = collision_map
        self.facing_angle = nav.get_angle_of_direction_between_points(self.current_pos, end_position[0])

        self.all_gradients = gradient_maps

        self.agent_weight = 1
        self.direction_cost = 200
        self.viewing_range = 1

        self.gradient_space_size = 4

        self.update_gradient(self.agent_weight)

        self.id = randint(0, 1000)

        self.anger = 0

        # added for graph map
        self.graph_map = deepcopy(gradient_maps[which_gradient_map])
        self.which_gradient_map = which_gradient_map
        self.number_reached = 0
        self.planning_range = 4
        self.number_to_reach = 2
        self.nr_directions = len(gradient_maps)

        # array that decides the chances for next movement
        # volgorde: garderobe, trap-garderobe, koffie, wc, randomlopen, eindlocatie
        self.chance_next = [[0, 0, 0.5, 0.1, 0.3, 0.1], [0, 0, 0.5, 0.1, 0.3, 0.1], [0, 0, 0, 0.3, 0.4, 0.3], [0, 0, 0.5, 0, 0.4, 0.1], [0, 0, 0.5, 0.2, 0, 0.3], [0, 0, 0, 0, 0, 0]]
        # tijdelijk voor testen
        self.chance_next2 = [[0.5, 0.5], [0.5, 0.5]]

    def update_facing_angle(self, new_pos):
        self.facing_angle = nav.get_angle_of_direction_between_points(self.current_pos, new_pos)

    # We're using the available moves from a position to navigate which blocks in the distance are also available
    def get_available_moves_from_tile(self, position):
        available_spots = []
        print("y ranges", (position[0]-1, position[0]+1))
        print("x ranges", range(position[1]-1, position[1]+1))
        # Last range is +2 because the range arg is exclusive the outermost range
        for y in range(position[0]-1, position[0]+2):
            for x in range(position[1]-1, position[1]+2):

                # If the point is the current square.
                if y == position[0] and x == position[1]:
                    continue

                # If we out of range we skip
                if y >= len(self.collision_map) or x >= len(self.collision_map[0]) or \
                        y <= 0 or x <= 0:
                    continue

                # Skip obstacles or EXITS as available moves
                if self.direction_map[y][x] == Env.OBSTACLE or self.direction_map[y][x] == Env.EXIT:
                    continue

                if self.collision_map[y][x] == Env.OBSTACLE or self.collision_map[y][x] == Env.EXIT:  # TODO check this validation and the 65 thing
                    continue

                available_spots.append((self.direction_map[y][x], (y, x)))

        available_spots.sort()

        return available_spots

    def get_viewable_moves(self, source, available_moves, visited, depth):
        # We always start looking at depth of 0, which is from the current agent tile.
        if depth is None:
            depth = 0

        # If we're out of sight, stop and return till where we can see
        if depth >= self.viewing_range:
            return available_moves  # TODO: We can also just keep it passby value, this is probably unneeded

        neighbours = self.get_available_moves_from_tile(source)

        for move in neighbours:
            if move not in visited:
                visited.add(move[1])  # only add the coord, not the weight
                depth += 1
                available_moves = self.get_viewable_moves(move[1], available_moves, visited, depth)
                available_moves.add((source, move))
                depth -= 1

        return available_moves

    def add_diagonal_weight_to_moves(self, available_moves):
        diagonal_weighted_moves = []
        for move in available_moves:
            source_step = move[0]
            weight = move[1][0]
            dest_step = move[1][1]

            if source_step[0] != dest_step[0] and source_step[1] != dest_step[1]:  # if diagonal, aka both y,x coords are different we add weight
                new_weight = weight + self.direction_cost #TODO: we could also do this as a percent of the sqaure weight
                move = (source_step, (new_weight, dest_step))

            diagonal_weighted_moves.append(move)

        return diagonal_weighted_moves

    def get_available_moves(self, current_position):
        # print("position", current_position)
        available_moves = self.get_viewable_moves(source=current_position, available_moves=set(), visited=set(), depth=None)

        # Agent is blocked even within viewing range.
        if available_moves is None:
            return None

        # Add diagonal weight to moves, to make agents want to keep walking forward instead of choosing to zigzag
        available_moves = self.add_diagonal_weight_to_moves(available_moves)

        print("current_position", current_position)
        print("avail moves:")
        for move in available_moves:
            print(move)

        next_step = trans.best_move(current_position, available_moves)
        # print(next_step)
        return next_step

    def get_best_move(self, available_spots: [(int, (int, int))]):

        if len(available_spots) == 0:
            return None

        for i in range(0, len(available_spots)):
            a_y, a_x = available_spots[i][1]
            if self.collision_map[a_y][a_x] == 0:
                return available_spots[i][1]

        return None

    def block_point(self, position):
        self.collision_map[position[0]][position[1]] = 1

    def unblock_point(self, position):
        self.collision_map[position[0]][position[1]] = 0

    def update_gradient(self, value):
        for y in range(-self.gradient_space_size, self.gradient_space_size + 1):
            for x in range(-self.gradient_space_size, self.gradient_space_size + 1):

                local_y = self.current_pos[0] + y
                local_x = self.current_pos[1] + x

                if y >= 5 or y <= -5 or x >= 5 or x <= -5:
                    tmp_value = int(value/5)
                elif y == 4 or y == -4 or x == 4 or x == -4:
                    tmp_value = int(value/4)
                elif y == 3 or y == -3 or x == 3 or x == -3:
                    tmp_value = int(value/3)
                elif y == 2 or y == -2 or x == 2 or x == -2:
                    tmp_value = int(value/2)
                else:
                    tmp_value = value

                # If we this is current spot we double value here
                if local_y == self.current_pos[0] and local_x == self.current_pos[1]:
                    for i in range(0, len(self.all_gradients)):
                        self.all_gradients[i][local_y][local_x] += tmp_value*2
                    continue

                # If we out of range we skip
                if local_y >= len(self.collision_map) or local_x >= len(self.collision_map[0]) or \
                        local_y <= 0 or local_x <= 0:
                    continue

                # If spot is obstacle or exit we skip
                if self.direction_map[local_y][local_x] == Env.EXIT or \
                        self.direction_map[local_y][local_x] == Env.OBSTACLE:
                    continue

                # Normal situation
                for i in range(0, len(self.all_gradients)):
                    self.all_gradients[i][local_y][local_x] += tmp_value * 2

    def move(self):

        best_pos = self.get_available_moves(self.current_pos)
        # print("bp", best_pos)

        if best_pos is None:
            # print("agent blocked")
            # self.value += self.value
            # self.update_gradient(self.value)
            return 0

        # TODO: no more than 2 agents in 1 sqaure, this should be extracted to other validation place.

        self.unblock_point(self.current_pos)

        if best_pos == Env.EXIT or self.direction_map[best_pos[0]][best_pos[1]] < 65:
            # self.number_reached += 1
            # if self.number_reached >= self.number_to_reach:
            #     self.update_gradient(-self.value)
            #
            #     raise ExitReached
            # else:

            # check if agent is at a location where it should be removed.
            # TODO: als alle maps er zijn: ook bij de tweede locatie verwijderen! want dat is die trappengang
            if self.which_gradient_map == len(self.all_gradients) - 1:
                # agent is at end location! remove.
                self.update_gradient(-self.agent_weight)
                raise ExitReached
            else:
                # chance of new direction depends on direction that was just finished
                new_direction = np.random.choice(2, 1, p=self.chance_next2[self.which_gradient_map])
                #print(new_direction)

                # new_direction = randint(0, self.nr_directions - 1)
                # while new_direction == self.which_gradient_map:
                #     new_direction = randint(0, self.nr_directions - 1)
                self.which_gradient_map = new_direction[0]
                # if self.which_gradient_map > 3:
                #     self.which_gradient_map = 0
                self.direction_map = self.all_gradients[self.which_gradient_map]
                self.graph_map = deepcopy(self.all_gradients[self.which_gradient_map])

        self.update_facing_angle(best_pos)

        self.update_gradient(-self.agent_weight)

        self.current_pos = best_pos
        self.block_point(self.current_pos)

        self.update_gradient(self.agent_weight)

        return 0


