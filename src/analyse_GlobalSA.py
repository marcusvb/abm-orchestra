
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import seaborn as sns

plt.style.use('ggplot')
def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure(dpi=120)

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')
    plt.tight_layout()


problem = {
    'num_vars': 3,
    'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
    'bounds': [[0.01, 0.4], [0.01, 0.3], [0.1, 0.5]]
}


output = pd.read_csv('Logs/Global_SA')
output.columns = ['id','Zuid Count', 'Noord ValidationCount', 'Champage ValidationCount', 'Noord Density','Zuid Density', 'Garderobe Density']
print(output.head())

x = output.sort_values(by=['id'])
print(x)


Si_zuid = sobol.analyze(problem, x['Zuid Count'][:96].as_matrix(), print_to_console=True)
Si_garderobe = sobol.analyze(problem, x['Garderobe Density'][:96].as_matrix(), print_to_console=True)


titles = ['Zuid Count', 'Garderobe Density']

for i, Si in enumerate([Si_zuid, Si_garderobe]):

    # First order

    plot_index(Si, problem['names'], '1', 'First order sensitivity: '+titles[i])
    # Total order
    plot_index(Si, problem['names'], 'T', 'Total order sensitivity: '+titles[i])

plt.show()





