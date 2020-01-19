import networkx as nx
import matplotlib.pyplot as plt

src = None
G = nx.Graph()

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
def dfs_furthest_seeing(G, visited, furthest_see_points, source=None, depth_limit=None, first=False):
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

            furthest_see_points, visited = dfs_furthest_seeing(G, visited, furthest_see_points, child, depth_limit)

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
    furthest_points, visited = dfs_furthest_seeing(G, visited=set(), furthest_see_points=set(), source=source,
                                                   first=True)

    #draw_graph(G, visited, furthest_points)
    print(len(G))

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


def best_move(source, move):
    global src, G
    src = source

    print("should always be 0:", len(G))
    G = generate_graph_from_grid_data(G, move)
    routes = find_routes_in_directions(G, source)
    G.clear() # clean the graph object

    #print("routes", routes)

    for path in routes:
        destination = path[0]
        weight = path[1][0] # lowest next step which is not itself
        go_to_path = path[1][1]

        if destination != source:
            for step in go_to_path:
                if step != source:
                    return step

    return None