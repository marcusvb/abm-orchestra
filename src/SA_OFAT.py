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
from gradient_main


# We define our variables and bounds
problem = {
    'num_vars': 3,
    'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
    'bounds': [[0.01, 0.5], [0.01, 0.5], [0.01, 0.5]]
}


# Generate samples
param_values = saltelli.sample(problem, 1000)

print(param_values)
#
for par in param_values:
    change params in MapConfs.py
    run gradient_main.py

