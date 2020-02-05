import numpy as np
from SALib.sample import saltelli

from gradient_main import GradientMain
from model.gradient_agent import MapConfs as mapConf

"""
Dependency management on OS for multiprocessing
"""
from sys import platform as _platform
if _platform == "win32" or _platform == "win64" or _platform == "darwin":
    import multiprocess
else:
    import multiprocessing as multiprocess


def Global_SA():
    # We define our variables and bounds
    problem = {
        'num_vars': 3,
        'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
        'bounds': [[0.01, 0.4], [0.01, 0.3], [0.1, 0.5]]
    }

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


def OFAT():
    # Generate samples
    sema = multiprocess.Semaphore(multiprocess.cpu_count())
    lock = multiprocess.Lock()

    jobs = []
    id_holder = 0

    distinct_samples = 20
    iterations = 100


    # We define our variables and bounds
    problem = {
        'num_vars': 3,
        'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
        'bounds': [[0.01, 0.4], [0.01, 0.3], [0.1, 0.5]]
    }

    Input = []

    for i, var in enumerate(problem['names']):
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples)
        Input.append(samples)
    # print(Input)
    # InputTranspose = np.transpose(Input)
    # print(InputTranspose)
    FixedValues = [0.1, 0.1, 0.1]

    for i, parametersamples in enumerate(Input):
        id_holder = 0

        for parsample in parametersamples:


            for j in range(iterations):
                # change params in MapConfs.py
                par = FixedValues
                par[i] = parsample

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
