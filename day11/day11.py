"""

Advent of Code 2025 - Day 11

"""

from collections import defaultdict
import networkx as nx
from functools import lru_cache


devices = defaultdict(list)
with open("day11.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        left, right = line.split(": ")
        devices[left] += right.split()

# Part 1

def find_all_paths(vertices, gList, source, destination):
    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    for u in gList:
        for v in gList[u]:
            G.add_edge(u, v)

    return list(nx.all_simple_paths(G, source=source, target=destination))

start_node = "you"
end_node = "out"
different_paths = find_all_paths(devices.keys(), devices, source=start_node, destination=end_node)

print(f'Advent of Code Day 11 Answer Part 1: {len(different_paths)}')

# Part 2

"""
pattern in the graph structure i.e. fft will always come before dac in the example input

- this means we can split the path counting into 3 segments:
    1. from start_node to all fft nodes
    2. from all fft nodes to all dac nodes
    3. from all dac nodes to end_node
    
Also, just count the # of paths, don't actually calculate the paths. You would run out of memory otherwise.
"""


start_node = "svr"
end_node = "out"

@lru_cache(None)
def find_paths(u, target=start_node):
    if u == target:
        return 1

    total = 0
    for neighbor in devices[u]:  # assumes there are no cycles
        total += find_paths(u=neighbor, target=target)

    return total

# svr -> fft
p1 = find_paths(start_node, target="fft")

# fft -> dac
p2 = find_paths("fft", target="dac")

# dac -> out
p3 = find_paths("dac", target=end_node)

print(f'Advent of Code Day 11 Answer Part 2: {p1 * p2 * p3}')
