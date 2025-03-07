def find_bridges_iterative(n: int, graph: list) -> int:
    """Для заданного графа с n вершинами выводим количество мостов в нём"""
    visited = [False] * n  # Список для флагов, посещена ли вершина
    k = [0] * n  # Время первого посещения для каждой вершины (k(v))
    l = [0] * n  # Минимальное значение k для каждой вершины, до которого можно добраться
    # из неё или из её поддерева с использованием обратных рёбер (l(v))
    parent = [-1] * n  # Родитель в дереве DFS для каждой вершины
    bridges = []
    timer = 1

    for start in range(n):
        # Учитываем что граф может быть не связным - проходим по всем вершинам
        if not visited[start]:
            stack = [(start, iter(graph[start]), 0)]  # Стек для итеративного DFS
            parent[start] = -1
            while stack:
                v, it, phase = stack.pop()  # phase - флаг фазы обработки вершины
                if phase == 0:
                    visited[v] = True
                    k[v] = timer
                    l[v] = timer
                    timer += 1
                    stack.append((v, it, 1))
                else:
                    try:
                        w = next(it)  # Переходим к следующему соседу w вершины v
                        if not visited[w]:
                            parent[w] = v
                            stack.append((v, it, 1))
                            stack.append((w, iter(graph[w]), 0))
                        else:
                            if w != parent[v]:
                                # Если w уже посещена и w не родитель v, то обновляем l(v)
                                l[v] = min(l[v], k[w])
                            stack.append((v, it, 1))
                    except StopIteration:
                        # Все соседи v обработаны
                        if parent[v] != -1:
                            # Если v не корень, то обновляем l(parent(v))
                            l[parent[v]] = min(l[parent[v]], l[v])
                            if l[v] > k[parent[v]]:
                                # Если true, значит обратного пути от v(или её поддерева)
                                # к p(или предкам p) нет -> мост
                                bridges.append((parent[v], v))
    return bridges


m = int(input().strip())
edges = []
max_vertex = -1

for _ in range(m):
    line = input().strip()
    u_str, v_str = line.split()
    u = int(u_str)
    v = int(v_str)
    edges.append((u, v))
    max_vertex = max(max_vertex, u, v)

n = max_vertex + 1

graph = [[] for _ in range(n)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

bridges = find_bridges_iterative(n, graph)
print(len(bridges))
