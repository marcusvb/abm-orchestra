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






class FixedBatchRunner(model_cls, parameters_list=None, fixed_parameters=None, iterations=1, max_steps=1000, model_reporters=None, agent_reporters=None, display_progress=True):
    """ This class is instantiated with a model class, and model parameters
    associated with one or more values. It is also instantiated with model and
    agent-level reporters, dictionaries mapping a variable name to a function
    which collects some data from the model or its agents at the end of the run
    and stores it.

    Note that by default, the reporters only collect data at the *end* of the
    run. To get step by step data, simply have a reporter store the model's
    entire DataCollector object.
    """
    def __init__(self, model_cls, parameters_list=None,
                 fixed_parameters=None, iterations=1, max_steps=100,
                 model_reporters=None, agent_reporters=None,
                 display_progress=True):
        """ Create a new BatchRunner for a given model with the given
        parameters.

        Args:
            model_cls: The class of model to batch-run.
            parameters_list: A list of dictionaries of parameter sets.
                The model will be run with dictionary of paramters.
                For example, given parameters_list of
                    [{"homophily": 3, "density": 0.8, "minority_pc": 0.2},
                    {"homophily": 2, "density": 0.9, "minority_pc": 0.1},
                    {"homophily": 4, "density": 0.6, "minority_pc": 0.5}]
                3 models will be run, one for each provided set of parameters.
            fixed_parameters: Dictionary of parameters that stay same through
                all batch runs. For example, given fixed_parameters of
                    {"constant_parameter": 3},
                every instantiated model will be passed constant_parameter=3
                as a kwarg.
            iterations: The total number of times to run the model for each set
                of parameters.
            max_steps: Upper limit of steps above which each run will be halted
                if it hasn't halted on its own.
            model_reporters: The dictionary of variables to collect on each run
                at the end, with variable names mapped to a function to collect
                them. For example:
                    {"agent_count": lambda m: m.schedule.get_agent_count()}
            agent_reporters: Like model_reporters, but each variable is now
                collected at the level of each agent present in the model at
                the end of the run.
            display_progress: Display progresss bar with time estimation?

        """
        self.model_cls = model_cls
        if parameters_list is None:
            parameters_list = []
        self.parameters_list = list(parameters_list)
        self.fixed_parameters = fixed_parameters or {}
        self._include_fixed = len(self.fixed_parameters.keys()) > 0
        self.iterations = iterations
        self.max_steps = max_steps

        self.model_reporters = model_reporters
        self.agent_reporters = agent_reporters

        if self.model_reporters:
            self.model_vars = {}

        if self.agent_reporters:
            self.agent_vars = {}

        self.display_progress = display_progress

    def _make_model_args(self):
        """Prepare all combinations of parameter values for `run_all`

        Returns:
            Tuple with the form:
            (total_iterations, all_kwargs, all_param_values)
        """
        total_iterations = self.iterations
        all_kwargs = []
        all_param_values = []

        count = len(self.parameters_list)
        if count:
            for params in self.parameters_list:
                kwargs = params.copy()
                kwargs.update(self.fixed_parameters)
                all_kwargs.append(kwargs)
                all_param_values.append(params.values())
        elif len(self.fixed_parameters):
            count = 1
            kwargs = self.fixed_parameters.copy()
            all_kwargs.append(kwargs)
            all_param_values.append(kwargs.values())

        total_iterations *= count

        return (total_iterations, all_kwargs, all_param_values)

    def run_all(self):
        """ Run the model at all parameter combinations and store results. """
        run_count = count()
        total_iterations, all_kwargs, all_param_values = self._make_model_args()

        with tqdm(total_iterations, disable=not self.display_progress) as pbar:
            for i, kwargs in enumerate(all_kwargs):
                param_values = all_param_values[i]
                for _ in range(self.iterations):
                    self.run_iteration(kwargs, param_values, next(run_count))
                    pbar.update()


    def run_iteration(self, kwargs, param_values, run_count):
        kwargscopy = copy.deepcopy(kwargs)
        model = self.model_cls(**kwargscopy)
        self.run_model(model)

        # Collect and store results:
        if param_values is not None:
            model_key = tuple(param_values) + (run_count,)
        else:
            model_key = (run_count,)

        if self.model_reporters:
            self.model_vars[model_key] = self.collect_model_vars(model)
        if self.agent_reporters:
            agent_vars = self.collect_agent_vars(model)
            for agent_id, reports in agent_vars.items():
                agent_key = model_key + (agent_id,)
                self.agent_vars[agent_key] = reports
        return (getattr(self, "model_vars", None), getattr(self, "agent_vars", None))

    def run_model(self, model):
        """ Run a model object to completion, or until reaching max steps.

        If your model runs in a non-standard way, this is the method to modify
        in your subclass.

        """
        while model.running and model.schedule.steps < self.max_steps:
            model.step()


    def collect_model_vars(self, model):
        """ Run reporters and collect model-level variables. """
        model_vars = {}
        for var, reporter in self.model_reporters.items():
            model_vars[var] = reporter(model)
        return model_vars


    def collect_agent_vars(self, model):
        """ Run reporters and collect agent-level variables. """
        agent_vars = {}
        for agent in model.schedule._agents.values():
            agent_record = {}
            for var, reporter in self.agent_reporters.items():
                agent_record[var] = getattr(agent, reporter)
            agent_vars[agent.unique_id] = agent_record
        return agent_vars


    def get_model_vars_dataframe(self):
        """ Generate a pandas DataFrame from the model-level variables
        collected.

        """
        return self._prepare_report_table(self.model_vars)


    def get_agent_vars_dataframe(self):
        """ Generate a pandas DataFrame from the agent-level variables
        collected.

        """
        return self._prepare_report_table(self.agent_vars,
                                          extra_cols=['AgentId'])


    def _prepare_report_table(self, vars_dict, extra_cols=None):
        """
        Creates a dataframe from collected records and sorts it using 'Run'
        column as a key.
        """
        extra_cols = ['Run'] + (extra_cols or [])
        index_cols = set()
        for params in self.parameters_list:
            index_cols |= params.keys()
        index_cols = list(index_cols) + extra_cols

        records = []
        for param_key, values in vars_dict.items():
            record = dict(zip(index_cols, param_key))
            record.update(values)
            records.append(record)

        df = pd.DataFrame(records)
        rest_cols = set(df.columns) - set(index_cols)
        ordered = df[index_cols + list(sorted(rest_cols))]
        ordered.sort_values(by='Run', inplace=True)
        if self._include_fixed:
            for param in self.fixed_parameters.keys():
                val = self.fixed_parameters[param]

                # avoid error when val is an iterable
                vallist = [val for i in range(ordered.shape[0])]
                ordered[param] = vallist
        return ordered
















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

    batch = FixedBatchRunner(model_cls=Model,
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={var: samples},
                        model_reporters=model_reporters,
                        display_progress=True)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()
