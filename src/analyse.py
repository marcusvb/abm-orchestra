import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import numpy as np

def plot_heatmap(map):
    # plt.figure(dpi=300)
    sns.heatmap(map, cmap='jet')
    plt.show()


def open_pickle(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


def loadall(filename):
    da = []
    with open(filename, "rb") as f:
        while True:
            try:
                data = pickle.load(f)
                da.append(data)
            except EOFError:
                break
    return da

items = loadall(r'Logs/Heatmap_pickle')
for heatmap in items:
    plot_heatmap(heatmap)
