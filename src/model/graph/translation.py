import networkx as nx


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
            furthest_see_points = dfs_furthest_seeing(G, child, depth_limit, visited=visited)

            # If only one neighbour next, in other words this is end of map sight range
            if len(list(nx.all_neighbors(G, child))) < 2:
                furthest_see_points.add(child)

    return furthest_see_points


# Sorts the possible paths based on the weight
def sort_on_weight(sub_li):
    sub_li.sort(key=lambda x: x[1][0])
    return sub_li


# Given the viewing graph, return which direction we need to step to
def find_routes_in_directions(G, source=None):
    furthest_points = dfs_furthest_seeing(G, source, first=True)

    paths = []
    for target in furthest_points:
        paths.append((target, nx.single_source_dijkstra(G, source, target, weight="weight")))

    return sort_on_weight(paths)
