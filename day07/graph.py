"""

Advent of Code 2025 - Day 7

"""

from collections import deque, defaultdict
import numpy as np
import functools
import networkx as nx


arr = []
with open("day07ex.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        arr.append([char for char in line])

arr = np.array(arr)

# Part 1

start_s = []
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        if arr[i, j] == 'S':
            start_s = (i, j)
            # useless to break here given python scopes, rust would be nice here

last_row = arr.shape[0] - 1
beams = deque([start_s])
splits = 0
graph = defaultdict(set)
while beams:
    current_beam = beams.popleft()
    if current_beam[0] + 1 > last_row:  # last row of grid
        continue

    r, c = current_beam[0] + 1, current_beam[1]
    if arr[r, c] == ".":  # clear path down
        beams.append([r, c])
        graph[(r - 1, c)].add((r, c))
    elif arr[r, c] == "^":  # split
        # test left split
        if c - 1 < 0:
            continue

        c -= 1
        if [r, c] not in beams:
            beams.append([r, c])
        graph[(r - 1, c + 1)].add((r, c))

        # test right split
        if c + 1 > arr.shape[1] - 1:
            continue

        c += 2
        if [r, c] not in beams:
            beams.append([r, c])
            splits += 1
        graph[(r - 1, c - 1)].add((r, c))

print(f'Advent of Code Day 7 Answer Part 1: {splits}')

# Part 2

# these solutions are way too slow though, need to go down a different path

def find_all_paths(vertices, gList, source, destination):
    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    for u in gList:
        for v in gList[u]:
            G.add_edge(u, v)

    return list(nx.all_simple_paths(G, source=source, target=destination))

for col in range(arr.shape[1]):
    graph[arr.shape[0] - 1, col] = set()

total = 0
for col in range(arr.shape[1]):
    to_search = (arr.shape[0] - 1, col)
    x = find_all_paths(graph.keys(), graph, source=start_s, destination=to_search)
    total += len(x)

# or

@functools.lru_cache(maxsize=None)
def dfs_all_paths(graph_items, start):
    graph = dict(graph_items)
    if not graph[start]:
        return [[start]]

    all_paths = []
    for neighbor in graph[start]:
        for path in dfs_all_paths(graph_items, neighbor):
            all_paths.append([start] + path)
    return all_paths

# lru_cache needs hashable types, so pass items as tuple

tuple_graph = graph
for key, value in graph.items():
    tuple_graph[key] = tuple(value)

paths = dfs_all_paths(tuple(tuple_graph.items()), start_s)
total = len(paths)

print(f'Advent of Code Day 7 Answer Part 2: {total}')
