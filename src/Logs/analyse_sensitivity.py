import pandas as pd
import matplotlib.pyplot as plt
from SALib.analyze import sobol
import pickle

# h = pickle.loads('Heatmap_pickle')
# plt.plot(h)
# plt.show()
#
def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
#
items = loadall('Heatmap_pickle')

for i in items:
    print(i)

# plt.style.use('ggplot')
# # We define our variables and bounds
# problem = {
#     'num_vars': 3,
#     'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
#     'bounds': [[0.1, 0.7], [0.1, 0.7], [0.1, 0.7]]
# }
#
#
# data = pd.read_csv('SA_data.txt')
# data.columns=['Validation Zuid', 'Validation Noord', 'Validation Champagne', 'Density Zuid', 'Density Noord', 'Density Garderobe']
#
# x = data['Validation Zuid'].as_matrix()[:96]
# Si_Zuid_Flux = sobol.analyze(problem, x,  print_to_console=False)
# x = data['Density Zuid'].as_matrix()[:96]
# Si_Zuid_Density = sobol.analyze(problem, x,  print_to_console=False)
#
# # x = data['Density Garderobe'].as_matrix()[:72]
# # Si_Garderobe_Density = sobol.analyze(problem, x,  print_to_console=False)
#
# def plot_index(s, params, i, title=''):
#     """
#     Creates a plot for Sobol sensitivity analysis that shows the contributions
#     of each parameter to the global sensitivity.
#
#     Args:
#         s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
#             the values for a set of parameters
#         params (list): the parameters taken from s
#         i (str): string that indicates what order the sensitivity is.
#         title (str): title for the plot
#     """
#
#     if i == '2':
#         p = len(params)
#         params = list(combinations(params, 2))
#         indices = s['S' + i].reshape((p ** 2))
#         indices = indices[~np.isnan(indices)]
#         errors = s['S' + i + '_conf'].reshape((p ** 2))
#         errors = errors[~np.isnan(errors)]
#     else:
#         indices = s['S' + i]
#         errors = s['S' + i + '_conf']
#         plt.figure()
#
#     l = len(indices)
#
#     plt.title(title)
#     plt.ylim([-0.2, len(indices) - 1 + 0.2])
#     plt.yticks(range(l), params)
#     plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
#     plt.axvline(0, c='k')
#     plt.tight_layout()
#
# plot_index(Si_Zuid_Density, problem['names'], 'T', 'Total order sensitivity: Zuid Density')
# plot_index(Si_Zuid_Density, problem['names'], '1', 'First order sensitivity')
# # plot_index(Si_Garderobe_Density, problem['names'], 'T', 'Total order sensitivity: Garderobe Density')
# # plot_index(Si_Garderobe_Density, problem['names'], '1', 'First order sensitivity')
# plot_index(Si_Zuid_Flux, problem['names'], 'T', 'Total order sensitivity: FLux Zuid')
# plot_index(Si_Zuid_Flux, problem['names'], '1', 'First order sensitivity')
# plt.show()
