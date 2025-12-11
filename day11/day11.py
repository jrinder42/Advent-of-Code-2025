"""

Advent of Code 2025 - Day 11

"""

from collections import defaultdict
import networkx as nx


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

print(f'Advent of Code Day 11 Answer Part 2: {1}')
