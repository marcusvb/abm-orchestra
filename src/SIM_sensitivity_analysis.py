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


def setup_confs_for_simulation(parameterMapConf):
    parameterMapConf.RunTime.RECORD_VIS = False  # Recording of frames
    parameterMapConf.RunTime.VISUALIZE = True
    parameterMapConf.RunTime.MAX_FRAMES = 8000
    parameterMapConf.RunTime.FINAL_STOP_FRAME = parameterMapConf.RunTime.MAX_FRAMES / 8
    parameterMapConf.RunTime.AGENTS = 2000
    parameterMapConf.RunTime.FRACTION = 1 / (3) * parameterMapConf.RunTime.AGENTS / parameterMapConf.RunTime.MAX_FRAMES

    parameterMapConf.RunTime.Z2_Q1 = parameterMapConf.RunTime.FRACTION * 1.25
    parameterMapConf.RunTime.Z2_Q2 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z2_Q3 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z2_Q4 = parameterMapConf.RunTime.FRACTION * 0.75

    parameterMapConf.RunTime.Z1_Q1 = parameterMapConf.RunTime.FRACTION * 1.25
    parameterMapConf.RunTime.Z1_Q2 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z1_Q3 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z1_Q4 = parameterMapConf.RunTime.FRACTION * 0.75

    return parameterMapConf


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
        # Setups the mapConf for this simulation
        parameterMapConf = setup_confs_for_simulation(mapConf)

        # Get the new parameters we're testing with SA
        parameterMapConf.Chances.AGENT_WEIGHT_PERCENT = par[0]
        parameterMapConf.Chances.ROUND_WALKING = par[1]
        parameterMapConf.Chances.TOILET = par[2]

        # Rescale the other chances, so that it all fits to 1
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


    FixedValues = [0.1, 0.1, 0.1]    #ground state of each variable during OFAT
    ParameterSamples = [0.01, 0.05, 0.1, 0.2, 0.5, 0.8]   #each parameter will be evaluated at these settings

    Parameters = ['agent_weight', 'random_walker_probability', 'toilet_probability']
    for i, Name in enumerate(Parameters):     #three loops for each input variable
        for Parameter in ParameterSamples:
                par = FixedValues
                par[i] = Parameter

                parameterMapConf = setup_confs_for_simulation(mapConf)

                parameterMapConf.Chances.AGENT_WEIGHT_PERCENT = par[0]
                parameterMapConf.Chances.ROUND_WALKING = par[1]
                parameterMapConf.Chances.TOILET = par[2]

                print("Params", "Agent_weight", par[0], "Round walk", par[1], "Toilet", par[2])

                SCALE_VARIABLE = parameterMapConf.Chances.TOILET + parameterMapConf.Chances.NOORD_ZUID + parameterMapConf.Chances.JUUL_BEA + parameterMapConf.Chances.SPIEGEL + parameterMapConf.Chances.CHAMP

                parameterMapConf.Chances.TOILET = parameterMapConf.Chances.TOILET / SCALE_VARIABLE
                parameterMapConf.Chances.NOORD_ZUID = parameterMapConf.Chances.NOORD_ZUID / SCALE_VARIABLE
                parameterMapConf.Chances.JUUL_BEA = parameterMapConf.Chances.JUUL_BEA / SCALE_VARIABLE
                parameterMapConf.Chances.SPIEGEL = parameterMapConf.Chances.SPIEGEL / SCALE_VARIABLE
                parameterMapConf.Chances.CHAMP = parameterMapConf.Chances.CHAMP / SCALE_VARIABLE

                sema.acquire()
                G = GradientMain(parameterMapConf)

                file_name = "OFAT_param_" + Name
                p = multiprocess.Process(target=G.run, args=(sema, lock, id_holder, False, file_name))
                jobs.append(p)
                p.start()
                id_holder += 1

    for p in jobs:
        p.join()


if __name__ == '__main__':
    # Global_SA()

    while True:
        OFAT()