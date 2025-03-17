def flag_first_type_edge(start, neighbor, edges, flows, caps):
    return (start, neighbor) in edges and flows[(start, neighbor)] < caps[(start, neighbor)]


def flag_second_type_edge(start, neighbor, edges, flows):
    return (neighbor, start) in edges and flows[(neighbor, start)] > 0


def dfs_find_path(graph, start, finish, path, caps, flows, edges, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            if flag_first_type_edge(start, neighbor, edges, flows, caps) or flag_second_type_edge(start, neighbor, edges, flows):
                if neighbor == finish:
                    path = path + [(start, neighbor)]
                    return path
                path_temp_res = dfs_find_path(graph, neighbor, finish, path + [(start, neighbor)], caps, flows, edges, visited=visited)
                if path_temp_res:
                    return path_temp_res


def ford_fulkerson(graph, caps, flows, edges, start, finish):
    max_flow = 0
    while True:
        path = dfs_find_path(graph, start, finish, [], caps, flows, edges, visited=None)
        if path is None:
            break

        path_caps = []
        for edge in path:
            if caps[edge] > 0:
                path_caps.append(caps[edge] - flows[edge])
            else:
                path_caps.append(-flows[edge])
        min_cap = min(path_caps)

        for u, v in path:
                flows[(u, v)] += min_cap
                flows[(v, u)] -= min_cap

        max_flow += min_cap
    return max_flow


m = int(input())
edges_list = []
caps_dict = {}
for _ in range(m):
    i, j, cap = input().split()
    edges_list.append((i, j))
    caps_dict[(i, j)] = int(cap)

extended_edges = edges_list.copy()
for (u, v) in edges_list:
    if (v, u) not in caps_dict:
        extended_edges.append((v, u))
        caps_dict[(v, u)] = 0
flows_dict = {(i, j): 0 for i, j in extended_edges}

graph_dict = {}
for u, v in extended_edges:
    if u not in graph_dict:
        graph_dict[u] = []
    graph_dict[u].append(v)

print(ford_fulkerson(graph_dict, caps_dict, flows_dict, edges_list, 's', 't'))

