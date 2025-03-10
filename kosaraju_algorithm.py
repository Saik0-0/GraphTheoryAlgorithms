from collections import defaultdict
from typing import Dict, List, Set


def reverse_graph(graph: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """Инвертируем рёбра в графе"""
    reversed_graph = defaultdict(list)
    for node in graph:
        for neighbor in graph[node]:
            reversed_graph[neighbor].append(node)
    return reversed_graph


def top_sort(graph: Dict[int, List[int]], node: int, visited: set, order: list):
    """Топологическая сортировка """
    visited.add(node)
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            top_sort(graph, neighbor, visited, order)
    order.append(node)


def dfs_stack(graph: Dict[int, List[int]], start: int, visited: set, component: list):
    """Алгоритм поиска в глубину через стек"""
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            component.append(vertex)
            for neighbor in reversed(graph.get(vertex, [])):
                if neighbor not in visited:
                    stack.append(neighbor)


def kosaraju_scc(graph: Dict[int, List[int]]) -> int:
    """Реализация алгоритма Касарайю для поиска компонент сильной связности в ориентированном графе"""
    reversed_graph = reverse_graph(graph)

    order = []
    visited = set()
    for node in graph:
        if node not in visited:
            top_sort(graph, node, visited, order)
    order.reverse()

    visited.clear()
    scc_count = 0
    for node in order:
        if node not in visited:
            component = []
            dfs_stack(reversed_graph, node, visited, component)
            scc_count += 1

    return scc_count


m = int(input())
graph = defaultdict(list)
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)

scc_count = kosaraju_scc(graph)
print(scc_count)
