from copy import deepcopy
import numpy as np

import model.navigator.navigator as nav
import model.graph.translation as trans
from model.agent.Agent import ExitReached

from model.environment.environment_enum import Env
from model.gradient_agent.RunConf import RunConf




class Agent:
    def __init__(self, start_position: (int, int), end_position: [(int, int)], gradient_maps,
                 collision_map: [[(int, int)]], stairs_garderobe, end_goal_frame, current_frame, moving_chance, MapConf, which_gradient_map=0, bound_size=2):
        self.start = start_position
        self.end = end_position
        self.wait_a_little = False
        self.current_pos = self.start
        self.front_collision_size = bound_size

        self.direction_map = gradient_maps[which_gradient_map]
        self.collision_map = collision_map
        self.facing_angle = nav.get_angle_of_direction_between_points(self.current_pos, end_position[0])
        self.all_gradients = gradient_maps
        self.all_directions = gradient_maps
        self.gradient_space_size = 4

        self.MapConf = MapConf

        self.PATHING_CONFIG = RunConf.GRADIENT
        self.GOAL_THRESHOLD = self.MapConf.MapConfs.GOAL_THRESHOLD
        self.anger = 0

        # added for graph map
        self.graph_map = deepcopy(gradient_maps[which_gradient_map])
        self.which_gradient_map = which_gradient_map
        self.nr_directions = len(gradient_maps)
        self.viewing_range = 2
        self.value = 10
        self.update_gradient(self.value)
        self.agent_weight_percent = self.MapConf.Chances.AGENT_WEIGHT_PERCENT
        self.go_to_path = None

        # to make sure everyone moves at their own pace
        self.moving_chance = moving_chance
        self.stairs_garderobe = stairs_garderobe
        self.end_goal_frame = end_goal_frame
        self.current_frame = current_frame

        # chances where to walk
        self.toilet_chance = self.MapConf.Chances.TOILET
        self.nz_chance = self.MapConf.Chances.NOORD_ZUID
        self.jb_chance = self.MapConf.Chances.JUUL_BEA
        self.spiegel_chance = self.MapConf.Chances.SPIEGEL
        self.champ_chance = self.MapConf.Chances.CHAMP
        self.round_walking_chance = self.MapConf.Chances.ROUND_WALKING

        # toilet waiting
        self.sitting_on_toilet = False
        self.current_toilettime = 0
        self.total_toilettime = 200

        # waiting for coatcheck
        self.waitingongarderobe = False
        self.current_coatchecktime = 0
        self.total_coatchecktime = 3

        # for the random moving and drink drinking
        self.round_nr = 0

        # for the random moving and drink drinking
        self.moving_random = False
        self.random_moves = 0
        self.max_random_moves = 0
        self.drinking_frames = 0
        self.min_random_steps = self.MapConf.Chances.MIN_RAND_STEPS
        self.max_random_steps = self.MapConf.Chances.MAX_RAND_STEPS
        self.max_drinking_frames = self.MapConf.Chances.DRINKING_FRAMES

    def update_facing_angle(self, new_pos):
        self.facing_angle = nav.get_angle_of_direction_between_points(self.current_pos, new_pos)

    def block_point(self, position):
        self.collision_map[position[0]][position[1]] = 1

    def unblock_point(self, position):
        self.collision_map[position[0]][position[1]] = 0

    def update_graph_map(self):
        self.graph_map = deepcopy(self.all_gradients[self.which_gradient_map]) # clean graphmap copy
        for y in range(self.current_pos[0]-self.viewing_range, self.current_pos[0]+self.viewing_range):
            for x in range(self.current_pos[1]-self.viewing_range, self.current_pos[1]+self.viewing_range):
                if y == self.current_pos[0] and x == self.current_pos[1]:
                    continue
                try:
                    if self.direction_map[y][x] == Env.OBSTACLE or self.direction_map[y][x] == Env.EXIT:
                        continue
                    else:
                        self.graph_map[y][x] = self.direction_map[y][x] + self.collision_map[y][x] * self.agent_weight_percent * self.direction_map[y][x] # Add a scale of the agent weight to the tile
                except:
                    continue

    def valid_step(self, step):
        y = step[0]
        x = step[1]

        # If we out of range we skip
        if y >= len(self.collision_map) or x >= len(self.collision_map[0]) or \
                y <= 0 or x <= 0:
            return False

        # Skip obstacles or EXITS as available moves
        if self.direction_map[y][x] == Env.OBSTACLE or self.direction_map[y][x] == Env.EXIT:
            return False

        if self.collision_map[y][x] == Env.OBSTACLE or self.collision_map[y][x] == Env.EXIT:  # TODO: check this
            return False

        return True

    def update_gradient(self, value):
        for y in range(-self.gradient_space_size, self.gradient_space_size + 1):
            for x in range(-self.gradient_space_size, self.gradient_space_size + 1):

                local_y = self.current_pos[0] + y
                local_x = self.current_pos[1] + x

                if y >= 5 or y <= -5 or x >= 5 or x <= -5:
                    tmp_value = int(value / 5)
                elif y == 4 or y == -4 or x == 4 or x == -4:
                    tmp_value = int(value / 4)
                elif y == 3 or y == -3 or x == 3 or x == -3:
                    tmp_value = int(value / 3)
                elif y == 2 or y == -2 or x == 2 or x == -2:
                    tmp_value = int(value / 2)
                else:
                    tmp_value = value

                # If we this is current spot we double value here
                if local_y == self.current_pos[0] and local_x == self.current_pos[1]:
                    for i in range(0, len(self.all_gradients)):
                        self.all_gradients[i][local_y][local_x] += tmp_value * 2
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

    def get_available_moves_from_tile_dijkstra(self, position):
        available_spots = []
        # Last range is +2 because the range arg is exclusive the outermost range
        for y in range(position[0]-1, position[0]+2):
            for x in range(position[1]-1, position[1]+2):

                # If the point is the current square.
                if y == position[0] and x == position[1]:
                    continue

                if self.valid_step((y, x)):
                    available_spots.append((self.graph_map[y][x], (y, x)))

        available_spots.sort() # returns the move with a weight.

        return available_spots

    def get_viewable_moves_dijkstra(self, source, available_moves, visited, depth):
        # We always start looking at depth of 0, which is from the current agent tile.
        if depth is None:
            depth = 0

        # If we're out of sight, stop and return till where we can see
        if depth >= self.viewing_range:
            return available_moves  # TODO: We can also just keep it passby value, this is probably unneeded

        neighbours = self.get_available_moves_from_tile_dijkstra(source)

        for move in neighbours:
            if move not in visited:
                visited.add(move[1])  # only add the coord, not the weight
                depth += 1
                available_moves = self.get_viewable_moves_dijkstra(move[1], available_moves, visited, depth)
                available_moves.add((source, move))
                depth -= 1

        return available_moves

    def get_available_moves_dijkstra(self, current_position):
        available_moves = self.get_viewable_moves_dijkstra(source=current_position, available_moves=set(), visited=set(), depth=None)

        # Agent is blocked even within viewing range.
        if available_moves is None:
            return None

        available_moves = list(available_moves)
        available_moves = trans.sort_on_weight(available_moves)
        next_step = trans.best_move(current_position, available_moves, self.viewing_range)
        return next_step

    def gen_step_and_return_next_step_dijkstra(self):
        self.go_to_path = self.get_available_moves_dijkstra(self.current_pos)
        if self.go_to_path is None:
            return None

        next_step = self.go_to_path.pop(0)
        if self.valid_step(next_step):
            return next_step

        return None

    def toiletbreak(self):
        self.current_toilettime += 1
        if self.current_toilettime == self.total_toilettime:
            self.sitting_on_toilet = False
            self.current_toilettime = 0
        return 0

    def garderobewait(self):
        self.current_coatchecktime += 1
        if self.current_coatchecktime == self.total_coatchecktime:
            self.waitingongarderobe = False
            self.current_coatchecktime = 0
        return 0


    def step_dijkstra(self):

        if self.go_to_path is None:
            best_pos = self.gen_step_and_return_next_step_dijkstra()
        elif len(self.go_to_path) == 0:
            # If we're done with our drijkstra run try gradient
            # If gradient fails, dijkstra will be called again and returns the next step
            self.PATHING_CONFIG = RunConf.GRADIENT
            self.go_to_path = None
            best_pos = self.run_gradient()
        else:
            next_step = self.go_to_path.pop(0)
            if self.valid_step(next_step):
                best_pos = next_step
            else:
                self.PATHING_CONFIG = RunConf.GRADIENT
                self.go_to_path = None
                best_pos = self.run_gradient()

        return best_pos

    def run_dijkstra(self):
        self.update_graph_map()
        best_pos = self.step_dijkstra()

        # Validation for agent that has no next move
        if best_pos is None:
            return 0

        # If dijkstra in dijkstra returns 0, aka super blocked, then agent stops.
        if best_pos == 0:
            return 0

        # Validation for not stepping on other agent if the next step is where an agent already is
        if self.collision_map[best_pos[0]][best_pos[1]]:
            return 0

        # Validations passed, move the agent
        self.unblock_point(self.current_pos)
        if best_pos == Env.EXIT or self.direction_map[best_pos[0]][best_pos[1]] < self.MapConf.MapConfs.GOAL_THRESHOLD:

            # check if agent is at a location where it should be removed.
            if self.which_gradient_map == len(self.all_gradients) - 1:
                # agent is at end location! remove.
                self.update_gradient(-self.value)
                raise ExitReached

            if 0 < self.which_gradient_map < 5 and self.random_moves == 0:
                # agent just got a drink, walk random to a random place
                self.moving_random = True
                self.max_random_moves = np.random.randint(self.min_random_steps, self.max_random_steps, 1)[0]

            # if agent went to directUpstairs, remove
            elif self.stairs_garderobe == 1:
                self.update_gradient(-self.value)
                raise ExitReached

            # if agent is currently walking in rounds, go to next location
            if 0 < self.round_nr < 4:
                new_direction = self.which_gradient_map + 1

                # go to the first location of the rounds
                if new_direction > 10:
                    new_direction = 7
                self.which_gradient_map = new_direction
                self.direction_map = self.all_gradients[self.which_gradient_map]

            else:
                # choose 1 of the directions in between or walk around if agent did not already
                chance = np.random.random()
                if chance < self.round_walking_chance and self.round_nr == 0:
                    self.round_nr = 1
                    new_direction = np.random.choice(len(self.all_gradients), 1,
                                                     p=[0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0])
                    self.which_gradient_map = new_direction[0]
                else:
                    new_direction = np.random.choice(len(self.all_gradients), 1,
                                                     p=[0, self.jb_chance, self.spiegel_chance, self.champ_chance,
                                                        self.nz_chance, self.toilet_chance / 2, self.toilet_chance / 2,
                                                        0, 0, 0, 0, 0])
                    self.which_gradient_map = new_direction[0]
                self.direction_map = self.all_gradients[self.which_gradient_map]

        # UPDATING ATTRIBUTES
        self.graph_map = deepcopy(self.all_gradients[self.which_gradient_map])

        self.update_facing_angle(best_pos)

        self.update_gradient(-self.value)

        self.current_pos = best_pos
        self.block_point(self.current_pos)

        self.update_gradient(self.value)

        return 0

    def get_available_moves_gradient(self):
        available_spots = []
        for y in range(self.current_pos[0] - 1, self.current_pos[0] + 2):
            for x in range(self.current_pos[1] - 1, self.current_pos[1] + 2):
                if self.valid_step((y, x)):
                    # if spot has lower gradient value then the current_pos we add it
                    if self.direction_map[y][x] < self.direction_map[self.current_pos[0]][self.current_pos[1]]:
                        available_spots.append((self.direction_map[y][x], (y, x)))

        available_spots.sort()
        return available_spots

    def get_best_move_gradient(self, available_spots: [(int, (int, int))]):

        if len(available_spots) == 0:
            return None

        for i in range(0, len(available_spots)):
            a_y, a_x = available_spots[i][1]
            if self.collision_map[a_y][a_x] == 0:
                return available_spots[i][1]

        return None

    def run_gradient(self):

        available_positions = self.get_available_moves_gradient()
        best_pos = self.get_best_move_gradient(available_positions)
        self.PATHING_CONFIG = RunConf.GRADIENT

        if best_pos is None:
            # self.PATHING_CONFIG = RunConf.DIJKSTRA   # Sets dijkstra running and calls the first dijkstra
            # return 0
            return self.run_dijkstra()

        self.unblock_point(self.current_pos)

        if best_pos == Env.EXIT or self.direction_map[best_pos[0]][best_pos[1]] < self.MapConf.MapConfs.GOAL_THRESHOLD:

            # check if agent is at a location where it should be removed.
            if self.which_gradient_map == len(self.all_gradients) - 1:
                # agent is at end location! remove.
                self.update_gradient(-self.value)
                raise ExitReached

            if self.which_gradient_map == 0:
                # agent has to wait for
                self.waitingongarderobe = True


            if 0 < self.which_gradient_map < 5 and self.random_moves == 0:
                # agent just got a drink, walk random to a random place
                self.moving_random = True
                self.max_random_moves = np.random.randint(self.min_random_steps, self.max_random_steps, 1)[0]

            if 4 < self.which_gradient_map < 7 and self.random_moves == 0:
                # agent just went to the bathroom, sits on the toilet
                self.sitting_on_toilet = True

            # if agent went to directUpstairs, remove
            elif self.stairs_garderobe == 1:
                self.update_gradient(-self.value)
                raise ExitReached

            # if agent is currently walking in rounds, go to next location
            if 0 < self.round_nr < 4:

                new_direction = np.random.choice([1,2,3,4], 1)
                # print(new_direction)

                # # go to the first location of the rounds
                # if new_direction > 10:
                #     new_direction = 7
                self.which_gradient_map = new_direction[0]


                self.direction_map = self.all_gradients[7 + self.which_gradient_map]

            else:
                # choose 1 of the directions in between or walk around if agent did not already
                chance = np.random.random()
                if chance < self.round_walking_chance and self.round_nr == 0:
                    self.round_nr = 1
                    new_direction = np.random.choice(len(self.all_gradients), 1,
                                                     p=[0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0])
                    self.which_gradient_map = new_direction[0]
                else:
                    new_direction = np.random.choice(len(self.all_gradients), 1,
                                                     p=[0, self.jb_chance, self.spiegel_chance, self.champ_chance,
                                                        self.nz_chance, self.toilet_chance / 2, self.toilet_chance / 2,
                                                        0, 0, 0, 0, 0])

                    self.which_gradient_map = new_direction[0]
                self.direction_map = self.all_gradients[self.which_gradient_map]



        self.update_facing_angle(best_pos)

        self.update_gradient(-self.value)

        self.current_pos = best_pos
        self.block_point(self.current_pos)

        self.update_gradient(self.value)

        return 0

    def get_random_moves(self):
        available_spots = []
        for y in range(self.current_pos[0] - 1, self.current_pos[0] + 2):
            for x in range(self.current_pos[1] - 1, self.current_pos[1] + 2):
                if self.valid_step((y, x)):
                    available_spots.append((self.direction_map[y][x], (y, x)))

        available_spots.sort()
        return available_spots

    def random_mover(self):
        available_spots = self.get_random_moves()
        moves = []
        for i in range(0, len(available_spots)):
            a_y, a_x = available_spots[i][1]
            if self.collision_map[a_y][a_x] == 0:
                moves.append(available_spots[i][1])

        if len(moves) == 0:
            return 0
        new_pos_nr = np.random.choice(len(moves), 1)[0]

        new_pos = moves[new_pos_nr]
        self.unblock_point(self.current_pos)
        self.update_facing_angle(new_pos)

        self.update_gradient(-self.value)

        self.current_pos = new_pos
        self.block_point(self.current_pos)

        self.update_gradient(self.value)

        return 0

    def walk_around_and_drink(self):
        # If we need to random move
        if self.drinking_frames < self.max_drinking_frames:
            if self.drinking_frames % 10 == 0 and not self.wait_a_little:
                self.wait_a_little = True
                self.random_mover()
            else:
                self.drinking_frames += 1
                self.wait_a_little = False
                return 0
        else:
            self.moving_random = False
            self.drinking_frames = 0
        return 0


    def move(self):
        self.current_frame += 1

        # go to end location if you should!
        if self.current_frame == self.end_goal_frame:
            self.which_gradient_map = len(self.all_gradients) - 1
            self.direction_map = self.all_directions[self.which_gradient_map]
            self.graph_map = deepcopy(self.all_gradients[self.which_gradient_map])

        move_chance = np.random.random()
        # moving_chance_nr = np.random.choice(self.moving_chance, 1)
        if move_chance > self.moving_chance:
            return 0


        #sitting on the toilet
        if self.sitting_on_toilet:
            return self.toiletbreak()

        #waiting on coat
        if self.waitingongarderobe:
            return self.garderobewait()

        if self.moving_random and self.current_frame < self.end_goal_frame:
            if self.random_moves <= self.max_random_moves:
                self.random_moves += 1
                return self.random_mover()
            else:

                # walked far enough, now drink your drink for 5 mins
                if self.drinking_frames < self.max_drinking_frames:
                    self.drinking_frames += 1
                    return 0

                # five mins are over, go to next goal in next frame
                else:
                    self.moving_random = False
                    self.drinking_frames = 0
                    self.random_moves = 0
                    return 0


        elif self.PATHING_CONFIG == RunConf.DIJKSTRA:
            return self.run_dijkstra()
        else:
            return self.run_gradient()



