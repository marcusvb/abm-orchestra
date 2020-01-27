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
    JUUL_BEA = 0.15
    SPIEGEL = 0.2
    CHAMP = 0.05

    SCALE_VARIABLE = TOILET + NOORD_ZUID + JUUL_BEA + SPIEGEL + CHAMP

    TOILET = TOILET / SCALE_VARIABLE
    NOORD_ZUID = NOORD_ZUID / SCALE_VARIABLE
    JUUL_BEA = JUUL_BEA / SCALE_VARIABLE
    SPIEGEL = SPIEGEL / SCALE_VARIABLE
    CHAMP = CHAMP / SCALE_VARIABLE

    ROUND_WALKING = 0.2


    MIN_RAND_STEPS = 5
    MAX_RAND_STEPS = 15
    DRINKING_FRAMES = int(1000/5)

    # used for the gradient map for dijkstra
    AGENT_WEIGHT_PERCENT = 0.10

class RunTime():

    VISUALIZE = False
    MAX_FRAMES = 1000
    FINAL_STOP_FRAME = MAX_FRAMES

    Z2_Q1 = 0.2
    Z2_Q2 = 0.15
    Z2_Q3 = 0.15
    Z2_Q4 = 0.1
    Z1_Q1 = 0.1
    Z1_Q2 = 0.075
    Z1_Q3 = 0.075
    Z1_Q4 = 0.05



