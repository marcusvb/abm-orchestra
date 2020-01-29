import glfw
from OpenGL.GL import *
import random
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


from SALib.sample import saltelli
# from SALib.analyze import sobol
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from gradient_main import GradientMain
from model.gradient_agent import MapConfs as mapConf
# import multiprocessing as multiprocess # Only voor CEOtje
import multiprocess



# # Set the repetitions, the amount of steps, and the amount of distinct values per variable
# replicates = 10
# max_steps = 100
# distinct_samples = 20
#
# # Set the outputs
# model_reporters = {"Wolves": lambda m: m.schedule.get_breed_count(Wolf),
#                    "Sheep": lambda m: m.schedule.get_breed_count(Sheep)}
#
# data = {}
#
# for i, var in enumerate(problem['names']):
#     # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
#     samples = np.linspace(*problem['bounds'][i], num=distinct_samples)
#
#     # Keep in mind that wolf_gain_from_food should be integers. You will have to change
#     # your code to acommidate for this or sample in such a way that you only get integers.
#     if var == 'wolf_gain_from_food':
#         samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype=int)
#
#     batch = BatchRunner(WolfSheep,
#                         max_steps=max_steps,
#                         iterations=replicates,
#                         variable_parameters={var: samples},
#                         model_reporters=model_reporters,
#                         display_progress=True)
#
#     batch.run_all()
#
#     data[var] = batch.get_model_vars_dataframe()







if __name__ == '__main__':
    # Generate samples
    sema = multiprocess.Semaphore(multiprocess.cpu_count())
    lock = multiprocess.Lock()

    jobs = []
    id_holder = 0

    distinct_samples = 20
    iterations = 10
    maxiter = 1000

    # We define our variables and bounds
    problem = {
        'num_vars': 3,
        'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
        'bounds': [[0.01, 0.4], [0.01, 0.3], [0.1, 0.5]]
    }

    Input = []

    for i in range(maxiter):
            parameterMapConf = mapConf

            parameterMapConf.Chances.AGENT_WEIGHT_PERCENT = 0.1      #ELINE, MAARTEN
            # parameterMapConf.Chances.AGENT_WEIGHT_PERCENT = 0.2     #ALI, MILOU

            parameterMapConf.RunTime.Z2_Q1 = parameterMapConf.RunTime.FRACTION * 1.3     #ELINE, ALI
            # parameterMapConf.RunTime.Z2_Q2 = parameterMapConf.RunTime.FRACTION
            # parameterMapConf.RunTime.Z2_Q3 = parameterMapConf.RunTime.FRACTION
            # parameterMapConf.RunTime.Z2_Q4 = parameterMapConf.RunTime.FRACTION * 0.7

            parameterMapConf.RunTime.Z2_Q1 = parameterMapConf.RunTime.FRACTION * 1.2   #MAARTEN, MILOU
            parameterMapConf.RunTime.Z2_Q2 = parameterMapConf.RunTime.FRACTION * 1.2
            parameterMapConf.RunTime.Z2_Q3 = parameterMapConf.RunTime.FRACTION
            parameterMapConf.RunTime.Z2_Q4 = parameterMapConf.RunTime.FRACTION * 0.6

            sema.acquire()
            G = GradientMain(parameterMapConf)

            p = multiprocess.Process(target=G.run, args=(sema, lock, id_holder))
            jobs.append(p)
            p.start()
            id_holder += 1

    for p in jobs:
        p.join()


    #
    # for par in Input:
    #
    #     for i in range(iterations):
    # # for par in param_values:
    # #     # change params in MapConfs.py
    # #
    #         parameterMapConf = mapConf
    #
    #         parameterMapConf.Chances.AGENT_WEIGHT_PERCENT = par[0]
    #         parameterMapConf.Chances.ROUND_WALKING = par[1]
    #         parameterMapConf.Chances.TOILET = par[2]
    #
    #         SCALE_VARIABLE = parameterMapConf.Chances.TOILET + parameterMapConf.Chances.NOORD_ZUID + parameterMapConf.Chances.JUUL_BEA + parameterMapConf.Chances.SPIEGEL + parameterMapConf.Chances.CHAMP
    #
    #         parameterMapConf.Chances.TOILET = parameterMapConf.Chances.TOILET / SCALE_VARIABLE
    #         parameterMapConf.Chances.NOORD_ZUID = parameterMapConf.Chances.NOORD_ZUID / SCALE_VARIABLE
    #         parameterMapConf.Chances.JUUL_BEA = parameterMapConf.Chances.JUUL_BEA / SCALE_VARIABLE
    #         parameterMapConf.Chances.SPIEGEL = parameterMapConf.Chances.SPIEGEL / SCALE_VARIABLE
    #         parameterMapConf.Chances.CHAMP = parameterMapConf.Chances.CHAMP / SCALE_VARIABLE
    #
    #         sema.acquire()
    #         G = GradientMain(parameterMapConf)
    #
    #         p = multiprocess.Process(target=G.run, args=(sema, lock, id_holder))
    #         jobs.append(p)
    #         p.start()
    #         id_holder += 1
    #
    # for p in jobs:
    #     p.join()
