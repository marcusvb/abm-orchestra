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
import multiprocessing as multiprocess # Only voor CEOtje
# import multiprocess





if __name__ == '__main__':
    # Generate samples
    sema = multiprocess.Semaphore(multiprocess.cpu_count())
    lock = multiprocess.Lock()

    jobs = []
    id_holder = 0

    iterations = 12

    proportionsZI = [3/10, 3/15]              #Push voor MILOU
    proportionsZII = [27/20, 42/30]
    # proportionsZI = [3/2, 1, 3/5, 3/10, 3/15]
    # proportionsZII = [3/4, 1, 12/10, 27/20, 42/30]

    for i, prop in enumerate(proportionsZI):
        for j in range(iterations):
            # change params in MapConfs.py


            parameterMapConf = mapConf


            parameterMapConf.RunTime.Z2_Q1 = parameterMapConf.RunTime.FRACTION * 1.25 * proportionsZII[i]
            parameterMapConf.RunTime.Z2_Q2 = parameterMapConf.RunTime.FRACTION * proportionsZII[i]
            parameterMapConf.RunTime.Z2_Q3 = parameterMapConf.RunTime.FRACTION * proportionsZII[i]
            parameterMapConf.RunTime.Z2_Q4 = parameterMapConf.RunTime.FRACTION * 0.75 * proportionsZII[i]

            parameterMapConf.RunTime.Z1_Q1 = parameterMapConf.RunTime.FRACTION * 1.25 * prop
            parameterMapConf.RunTime.Z1_Q2 = parameterMapConf.RunTime.FRACTION * prop
            parameterMapConf.RunTime.Z1_Q3 = parameterMapConf.RunTime.FRACTION * prop
            parameterMapConf.RunTime.Z1_Q4 = parameterMapConf.RunTime.FRACTION * 0.75 * prop

            sema.acquire()
            G = GradientMain(parameterMapConf)

            p = multiprocess.Process(target=G.run, args=(sema, lock, id_holder))
            jobs.append(p)
            p.start()
            id_holder += 1

    for p in jobs:
        p.join()
