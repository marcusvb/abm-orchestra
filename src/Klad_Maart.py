from resources.handling.reading import load_direction_from_file, load_map_from_file

map_filename = "resources/ready/galeria_krakowska_maze100x100.txt"

maze_original = load_map_from_file(map_filename)
maze = load_map_from_file(map_filename)


def heatmap_from_map(map):
    heatmap = []
    for i, row in enumerate(map):
        heatrow=[]
        for j, col in enumerate(row):
            if col == 0:
                heatrow.append(1)
            elif col == 1:
                heatrow.append(0)

            else:
                raise 'ValueError'   #initial map should contain only 0 and 1
        heatmap.append(heatrow)
    return heatmap

print(heatmap_from_map(maze))