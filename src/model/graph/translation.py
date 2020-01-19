import networkx as nx
import matplotlib.pyplot as plt

src = None

def draw_graph(G, visited, outter):
    edges = []
    for n1, n2, attr in G.edges(data=True):
        attrs = (n1, n2, attr["weight"])
        edges.append(attrs)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=100)
    nx.draw_networkx_edges(G, pos, edgelist=edges)
    nx.draw_networkx_labels(G, pos)


    for v in visited:
        nx.draw_networkx_nodes(G, pos, nodelist=[v], node_color='g')

    for e in outter:
        nx.draw_networkx_nodes(G, pos, nodelist=[e], node_color='r')

    nx.draw_networkx_nodes(G, pos, nodelist=[src], node_color='y')

    # nx.draw_networkx_edge_labels(G, pos)
    plt.show()
    plt.clf()

# Returns a set of the furthest seeing points.
def dfs_furthest_seeing(G, source=None, depth_limit=None, visited=set(), furthest_see_points=set(), first=False):
    # Always add the first source to visited, TODO: maybe remove and re-write this.
    if first:
        visited.add(source)

    # No depth limits as our viewing-range is dictated by the framework
    if depth_limit is None:
        depth_limit = len(G)

    neighbours = list(nx.all_neighbors(G, source))
    for child in neighbours:
        if child not in visited:
            visited.add(child)

            furthest_see_points, _ = dfs_furthest_seeing(G, child, depth_limit, visited=visited)

            # If only one neighbour next, in other words this is end of map sight range
            if len(list(nx.all_neighbors(G, child))) < 2:
                furthest_see_points.add(child)

    return furthest_see_points, visited


# Sorts the possible paths based on the weight
def sort_on_weight(sub_li):
    sub_li.sort(key=lambda x: x[1][0])
    return sub_li


# Given the viewing graph, return which direction we need to step to
def find_routes_in_directions(G, source=None):
    furthest_points, visited = dfs_furthest_seeing(G, source, first=True)

    draw_graph(G, visited, furthest_points)

    paths = []
    for target in furthest_points:
        paths.append((target, nx.single_source_dijkstra(G, source, target, weight="weight")))

    return sort_on_weight(paths)


def viewable_weighted_moves_to_graph(moves):
    G = nx.Graph()  # networkx graph init
    for source_move in moves:
        G.add_edges_from([
            (source_move[0], source_move[1][1])  # 0'th is the source, 1 is (weight, dest)
        ], weight=source_move[1][0])  # push weight attribute on edge
    return G


def best_move(move, source):
    global src
    src = source

    G = viewable_weighted_moves_to_graph(move)
    routes = find_routes_in_directions(G, source)
    # G = None

    best_move = routes[0]
    for path in best_move[1][1]:  #  weight: shortest_path, [1][1] here refers to the shortest path, instead of the source
        if path != source:
            return path