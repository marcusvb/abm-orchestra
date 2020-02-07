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

"""
Eveyting divided by 4 due to computational limits and having to do multiple runs for stochasticity
"""
def setup_confs_for_simulation(parameterMapConf):
    parameterMapConf.RunTime.RECORD_VIS = False  # Recording of frames
    parameterMapConf.RunTime.VISUALIZE = True
    parameterMapConf.RunTime.MAX_FRAMES = 2000
    parameterMapConf.RunTime.FINAL_STOP_FRAME = parameterMapConf.RunTime.MAX_FRAMES + 300  # (plus 200 here is to give time for agents to go to their places)
    parameterMapConf.RunTime.AGENTS = 500
    parameterMapConf.RunTime.FRACTION = 1 / (3) * parameterMapConf.RunTime.AGENTS / parameterMapConf.RunTime.MAX_FRAMES # 500 visitors fraction that enters is the total number of visitors divided by the number of frames

    parameterMapConf.RunTime.Z2_Q1 = parameterMapConf.RunTime.FRACTION * 1.25
    parameterMapConf.RunTime.Z2_Q2 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z2_Q3 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z2_Q4 = parameterMapConf.RunTime.FRACTION * 0.75

    parameterMapConf.RunTime.Z1_Q1 = parameterMapConf.RunTime.FRACTION * 1.25
    parameterMapConf.RunTime.Z1_Q2 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z1_Q3 = parameterMapConf.RunTime.FRACTION
    parameterMapConf.RunTime.Z1_Q4 = parameterMapConf.RunTime.FRACTION * 0.75

    return parameterMapConf


def run_sim(new_entrance):
    # Generate samples
    sema = multiprocess.Semaphore(multiprocess.cpu_count())
    lock = multiprocess.Lock()
    jobs = []
    id_holder = 0

    for _ in range(multiprocess.cpu_count()):
        # Setup the MapConf for this simulation
        parameterMapConf = setup_confs_for_simulation(mapConf)

        sema.acquire()
        G = GradientMain(parameterMapConf)

        p = multiprocess.Process(target=G.run, args=(sema, lock, id_holder, new_entrance))

        jobs.append(p)
        p.start()
        id_holder += 1

    count = 0
    for p in jobs:
        count += 1
        p.join()
        print("jobs done...", count)

if __name__ == '__main__':
    while True:
        # Old entrance
        run_sim(False)
        # New entrance
        run_sim(True)
