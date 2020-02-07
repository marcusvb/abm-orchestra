

import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import numpy as np

def plot_heatmap(map):
    plt.figure(dpi=100)
    sns.heatmap(map, cmap='jet')
    plt.show()


def open_pickle(filename):
    pickle_list = []
    with open(filename, 'rb') as handle:

        return pickle.load(handle)


heatmaps = open_pickle(r'Logs/Heatmap_pickles')
print(len(heatmaps))
i = 0
plot_heatmap(heatmaps)


# print(heatmaps)

