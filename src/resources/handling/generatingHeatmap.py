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