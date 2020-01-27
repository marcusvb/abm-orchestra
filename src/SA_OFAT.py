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
import multiprocessing as multiprocess


# We define our variables and bounds
problem = {
    'num_vars': 3,
    'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
    'bounds': [[0.1, 0.7], [0.1, 0.7], [0.1, 0.7]]
}


if __name__ == '__main__':   
    # Generate samples
    param_values = saltelli.sample(problem, 1000)
    sema = multiprocess.Semaphore(multiprocess.cpu_count())
    lock = multiprocess.Lock()

    jobs = []
    id_holder = 0
    for par in param_values:
        # change params in MapConfs.py

        parameterMapConf = mapConf

        parameterMapConf.Chances.AGENT_WEIGHT_PERCENT = par[0]
        parameterMapConf.Chances.ROUND_WALKING = par[1]
        parameterMapConf.Chances.TOILET = par[2]

        SCALE_VARIABLE = parameterMapConf.Chances.TOILET + parameterMapConf.Chances.NOORD_ZUID + parameterMapConf.Chances.JUUL_BEA + parameterMapConf.Chances.SPIEGEL + parameterMapConf.Chances.CHAMP

        parameterMapConf.Chances.TOILET = parameterMapConf.Chances.TOILET / SCALE_VARIABLE
        parameterMapConf.Chances.NOORD_ZUID = parameterMapConf.Chances.NOORD_ZUID / SCALE_VARIABLE
        parameterMapConf.Chances.JUUL_BEA = parameterMapConf.Chances.JUUL_BEA / SCALE_VARIABLE
        parameterMapConf.Chances.SPIEGEL = parameterMapConf.Chances.SPIEGEL / SCALE_VARIABLE
        parameterMapConf.Chances.CHAMP = parameterMapConf.Chances.CHAMP / SCALE_VARIABLE

        sema.acquire()
        G = GradientMain(parameterMapConf)

        p = multiprocess.Process(target=G.run, args=(sema, lock, id_holder))
        jobs.append(p)
        p.start()
        id_holder += 1

    for p in jobs:
        p.join()
