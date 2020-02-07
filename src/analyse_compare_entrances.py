import pickle

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.style.use('ggplot')

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

def heatmapportion(map, yi, ye, xi, xe):
    portion = []
    map = map[yi:ye]
    for row in map:
        portion.append(row[xi:xe])

    flat_list = [item for sublist in portion for item in sublist]

    high = len(flat_list)//70  # used for highest 10% from heatmap
    high_portion = sorted(flat_list, reverse = True)[:high]  # sort the heatmap and take highest 10%
    # print(len(high_portion))

    return np.mean(high_portion)


"""
We load the data from the comapare entrances, 
extract the ten most busy points of the runs for both
North and South entrances. These are box-plotted 
to see if we have a significant difference. 
"""

items = loadall(r'Logs/Heatmap_pickle_entrance_False')
boxplot1 = []
for heatmap in items:
    # plot_heatmap(heatmap)
    heatmap_portion = heatmapportion(heatmap, 57, 141, 81, 90)
    boxplot1.append(heatmap_portion)

items = loadall(r'Logs/Heatmap_pickle_entrance_True')
boxplot2 = []
for heatmap in items:
    # plot_heatmap(heatmap)
    heatmap_portion = heatmapportion(heatmap, 57, 141, 81, 90)
    boxplot2.append(heatmap_portion)

plt.figure(dpi=120)
box = plt.boxplot([boxplot1, boxplot2], patch_artist=True, labels=['Zuid Entrance', 'Noord Entrance'])
plt.ylabel('Average number of agents')
plt.title('Ten most crowded grid spaces in the cloakroom area \n')


colors = ['lightblue', 'lightgreen']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
plt.savefig('plots/Boxplot_heatmaps.png')
plt.show()