from gradient_main import GradientMain
from model.gradient_agent import MapConfs as mapConf

"""
Dependency management on OS for multiprocessing
"""
from sys import platform as _platform
if _platform == "win32" or _platform == "win64" or _platform == "darwin":
    import multiprocessing as multiprocess
else:
    import multiprocess

# TODO: the proportions arents looking right
def get_proportions(new_entrance):
    return [1], [1]
    # if new_entrance:
    #     return [3/2, 1, 3/5, 3/10, 3/15], [3/4, 1, 12/10, 27/20, 42/30]
    # return [3/10, 3/15], [27/20, 42/30]

def run_sim(new_entrance):
    # Generate samples
    sema = multiprocess.Semaphore(multiprocess.cpu_count())
    lock = multiprocess.Lock()
    jobs = []
    id_holder = 0

    iterations = 10

    # Change this if we want the New entrance
    proportionsZI, proportionsZII = get_proportions(new_entrance)

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
    # Old entrance
    run_sim(False)
    # New entrance
    run_sim(True)
