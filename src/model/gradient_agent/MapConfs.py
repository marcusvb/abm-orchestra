from enum import IntEnum


class MapConfs(IntEnum):
    GOAL_THRESHOLD = 65


class Chances():

    # chance for end goal
    TORENTJE = 0.14
    STAIRS_GARDEROBE = 0.05
    BACK_ENTRANCE = 1/3


    # chances where to go
    TOILET = 0.2
    NOORD_ZUID = 0.4
    JUUL_BEA = 0.2
    SPIEGEL = 0.15
    CHAMP = 0.05
    ROUND_WALKING = 0.1
    MIN_RAND_STEPS = 5
    MAX_RAND_STEPS = 15
    DRINKING_FRAMES = 1000

    # used for the gradient map for dijkstra
    AGENT_WEIGHT_PERCENT = 0.10

class RunTime():

    MAX_FRAMES = 1000
    Z2_Q1 = 0.2
    Z2_Q2 = 0.15
    Z2_Q3 = 0.15
    Z2_Q4 = 0.1
    Z1_Q1 = 0.1
    Z1_Q2 = 0.075
    Z1_Q3 = 0.075
    Z1_Q4 = 0.05



