import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

src = None
G = nx.Graph()
viewing_range = None

def draw_graph(G, outer, path=None):
    edges = []
    for n1, n2, attr in G.edges(data=True):
        attrs = (n1, n2, attr["weight"])
        edges.append(attrs)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=100)
    nx.draw_networkx_edges(G, pos, edgelist=edges)
    nx.draw_networkx_labels(G, pos)

    if outer is not None:
        for e in outer:
            nx.draw_networkx_nodes(G, pos, nodelist=[e], node_color='r')

    # Start point and edge labels
    nx.draw_networkx_nodes(G, pos, nodelist=[src], node_color='y')
    nx.draw_networkx_edge_labels(G, pos)

    if path is not None:
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='r')

    plt.show()

def dfs_furthest_seeing_fixed(G, source):
    # We always start looking at depth of 0, which is from the current agent tile.
    min_x = None
    max_x = None
    for node in list(G.nodes):
        x = node[1]
        # Set for first time
        if min_x is None and max_x is None:
            min_x = x
            max_x = x

        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x

    furthest_see_points = set()
    for x_iter in (min_x, source[1], max_x): # min_x, source_x and max_x
        min_y = None
        max_y = None

        # current column
        for node in list(G.nodes):
            node_y = node[0]
            node_x = node[1]

            if node_x == x_iter:
                if min_y is None and max_y is None:
                    min_y = node_y
                    max_y = node_y
                else:
                    if node_y < min_y:
                        min_y = node_y
                    if node_y > max_y:
                        max_y = node_y

        # For this column we append the min and maxes
        furthest_see_points.add((min_y, x_iter))
        furthest_see_points.add((max_y, x_iter))

    return furthest_see_points


# Sorts the possible paths based on the weight
def sort_on_weight(sub_li):
    sub_li.sort(key=lambda x: (x[1][0]))
    return sub_li

def sort_on_diagonals(sub_li):
    sub_li.sort(key=lambda x: (x[2]))
    return sub_li


# Given the viewing graph, return which direction we need to step to
def find_routes_in_directions(G, source=None):
    # furthest_points, visited = dfs_furthest_seeing_(G, visited=set(), furthest_see_points=set(), source=source,
    #                                                first=True)
    furthest_points = dfs_furthest_seeing_fixed(G, source)

    # non_transient = visited.difference(furthest_points)
    # transient = visited.difference(furthest_points)

    # draw_graph(G, None, furthest_points, path=None)

    paths = []
    for target in furthest_points:
        paths.append((target, nx.single_source_dijkstra(G, source, target, weight="weight")))

    return sort_on_weight(paths)


def generate_graph_from_grid_data(G, moves):
    for source_move in moves:
        G.add_edges_from([
            (source_move[0], source_move[1][1])  # 0'th is the source, 1 is (weight, dest)
        ], weight=source_move[1][0])  # push weight attribute on edge
    return G


def sort_weights_if_multiple_by_straight_first(source, routes):
    lowest_weight = None
    lowest_weights = []
    for path in routes:
        destination = path[0]
        weight = path[1][0]
        go_to_path = path[1][1]

        # Filter out bs, only good paths
        if destination != source:

            # Check if first for weight, else if there is a weight diff we break because we'll find suboptimal
            if lowest_weight is None:
                lowest_weight = weight
            elif lowest_weight != weight:
                break

            for step in go_to_path:
                if step != source:
                    diff = np.abs(step[0] - source[0]) + np.abs(step[1] - source[1])
                    lowest_weights.append((destination, (weight, go_to_path), diff))

    return sort_on_diagonals(lowest_weights)


def best_move(source, move, view_range):
    global src, G, viewing_range
    src = source
    viewing_range = view_range

    G = generate_graph_from_grid_data(G, move)
    routes = find_routes_in_directions(G, source)


    if routes is None:
        return None

    diff_routes = sort_weights_if_multiple_by_straight_first(source, routes)
    draw_graph(G, None, diff_routes[0][1][1])
    
    G.clear()  # clean the graph object

    # print("current agent_pos", source)
    # print("routes", routes)
    # print("diff_routes", diff_routes)

    for path in diff_routes:
        destination = path[0]
        weight = path[1][0]  # lowest next step which is not itself
        go_to_path = path[1][1]

        # Filter junk weights
        if destination != source:
            go_to_path.pop(0) # delete the first which networkx always returns
            return go_to_path
