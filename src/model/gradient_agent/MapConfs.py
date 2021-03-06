from enum import IntEnum


class MapConfs(IntEnum):
    GOAL_THRESHOLD = 65

class Chances():

    # chance for end goal
    TORENTJE = 0.14
    STAIRS_GARDEROBE = 0.05
    BACK_ENTRANCE = 1/3

    # chances where to go
    TOILET = 0.15
    NOORD_ZUID = 0.4
    JUUL_BEA = 0.15
    SPIEGEL = 0.2
    CHAMP = 0.10

    SCALE_VARIABLE = TOILET + NOORD_ZUID + JUUL_BEA + SPIEGEL + CHAMP

    TOILET = TOILET / SCALE_VARIABLE
    NOORD_ZUID = NOORD_ZUID / SCALE_VARIABLE
    JUUL_BEA = JUUL_BEA / SCALE_VARIABLE
    SPIEGEL = SPIEGEL / SCALE_VARIABLE
    CHAMP = CHAMP / SCALE_VARIABLE


    ROUND_WALKING = 0.1

    MIN_RAND_STEPS = 5
    MAX_RAND_STEPS = 15
    DRINKING_FRAMES = 150

    # used for the gradient map for dijkstra
    AGENT_WEIGHT_PERCENT = 0.05

class RunTime():

    """
    To compile to mp4 run command in the images folder:
    ffmpeg -r 30 -f image2 -s 1920x1080 -i pic%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
    see https://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/ for args
    """
    RECORD_VIS = False  # Recording of frames
    VISUALIZE = True
    MAX_FRAMES = 2000
    FINAL_STOP_FRAME = MAX_FRAMES + 300 # (plus 200 here is to give time for agents to go to their places)
    AGENTS = 500
    FRACTION = 1/(3) * AGENTS / MAX_FRAMES  #500 visitors fraction that enters is the total number of visitors divided by the number of frames

    #1/3 comes from the fact that in gradient_main.py 2 people enter Z2 and 1 person enters Z1 if sample is less than the probability FRACTION




    Z2_Q1 = FRACTION * 1.25
    Z2_Q2 = FRACTION
    Z2_Q3 = FRACTION
    Z2_Q4 = FRACTION * 0.75

    Z1_Q1 = FRACTION * 1.25
    Z1_Q2 = FRACTION
    Z1_Q3 = FRACTION
    Z1_Q4 = FRACTION * 0.75

    # Z2_Q1 = FRACTION * 1.2
    # Z2_Q2 = FRACTION * 1.2
    # Z2_Q3 = FRACTION
    # Z2_Q4 = FRACTION * 0.6
    #
    #
    # Z1_Q1 = FRACTION * 1.2
    # Z1_Q2 = FRACTION * 1.2
    # Z1_Q3 = FRACTION
    # Z1_Q4 = FRACTION * 0.6


