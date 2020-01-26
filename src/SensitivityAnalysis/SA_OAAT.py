import glfw
from OpenGL.GL import *
import random
import seaborn as sns
import matplotlib.pyplot as plt

from gfx.MazeTexture import MazeTexture
from model.direction_map.DirectionMap import DirectionMap
from model.environment.line import Point
from gfx.AgentManager import AgentManager
from resources.handling.reading import load_direction_from_file, load_map_from_file
from resources.handling.generatingHeatmap import heatmap_from_map
from model.gradient.gradient_map import gradient_from_direction_map
from model.gradient_agent.MapConfs import RunTime

import os
import sys
import pandas as pd
import numpy as np


from SALib.sample import saltelli
from SALib.analyze import sobol
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
import gradient_main as Model



# We define our variables and bounds
problem = {
    'num_vars': 3,
    'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
    'bounds': [[0.01, 0.5], [0.01, 0.5], [0.01, 0.5]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 100
distinct_samples = 10

# Set the outputs
model_reporters = {"Density Garderobe": Model.Density_dataframe['Density Garderobe'],
                   "Flux Zuid": Model.Validation_dataframe['Validation Zuid']}

data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

    # # Keep in mind that wolf_gain_from_food should be integers. You will have to change
    # # your code to acommidate for this or sample in such a way that you only get integers.
    # if var == 'wolf_gain_from_food':
    #     samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype=int)

    batch = BatchRunner(Model,
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={var: samples},
                        model_reporters=model_reporters,
                        display_progress=True)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()
