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


def run_sim(new_entrance):
    # Generate samples
    sema = multiprocess.Semaphore(multiprocess.cpu_count())
    lock = multiprocess.Lock()
    jobs = []
    id_holder = 0

    iters = 50
    for _ in range(iters):
        # change params in MapConfs.py
        parameterMapConf = mapConf

        parameterMapConf.RunTime.Z2_Q1 = parameterMapConf.RunTime.FRACTION * 1.25
        parameterMapConf.RunTime.Z2_Q2 = parameterMapConf.RunTime.FRACTION
        parameterMapConf.RunTime.Z2_Q3 = parameterMapConf.RunTime.FRACTION
        parameterMapConf.RunTime.Z2_Q4 = parameterMapConf.RunTime.FRACTION * 0.75

        parameterMapConf.RunTime.Z1_Q1 = parameterMapConf.RunTime.FRACTION * 1.25
        parameterMapConf.RunTime.Z1_Q2 = parameterMapConf.RunTime.FRACTION
        parameterMapConf.RunTime.Z1_Q3 = parameterMapConf.RunTime.FRACTION
        parameterMapConf.RunTime.Z1_Q4 = parameterMapConf.RunTime.FRACTION * 0.75

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
