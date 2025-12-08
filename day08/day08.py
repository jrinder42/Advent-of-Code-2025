"""

Advent of Code 2025 - Day 8

"""

from ast import literal_eval
from collections import defaultdict, Counter, deque
from itertools import combinations
import math


arr = []
with open("day08.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        arr.append([literal_eval(num) for num in line.split(",")])

# Part 1

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])** 2 + (p1[1] - p2[1])** 2 + (p1[2] - p2[2])**2)

boxes = {}
for box1, box2 in combinations(arr, 2):
    left, right = sorted([box1, box2], key=lambda x: (x[0], x[1], x[2]))
    left, right = tuple(left), tuple(right)
    dist = euclidean_distance(box1, box2)
    boxes[(left, right)] = dist

boxes = dict(sorted(boxes.items(), key=lambda x: x[1]))  # distances

circuits = defaultdict(set)
for idx, (key, value) in enumerate(boxes.items()):
    left, right = key
    circuits[left].add(right)
    circuits[right].add(left)

    if idx == 1000-1:  # make this 10-1 for the test input, 1000-1 for the real input
        break

# merge circuits
for key, value in circuits.items():
    for val in value:
        diff = value - set(val)
        diff.update({key})
        circuits[val].update(diff)

# lengths of circuits
to_ignore = set()
sizes = []
for key, value in circuits.items():
    if key in to_ignore:
        continue

    to_ignore.update(value)
    sizes.append(len(value))

# final aggregation of the top 3 largest circuits
freq = Counter(sizes)
freq_tuple = sorted(freq.keys())[-3:]
top = deque(freq_tuple[::-1])
prod = []
while len(prod) < 3:
    num = top.popleft()
    while freq[num] > 0:
        prod.append(num)
        freq[num] -= 1

prod = prod[:3]

print(f'Advent of Code Day 8 Answer Part 1: {math.prod(prod)}')

# Part 2

last_junction = None
circuits = []
for idx, (key, value) in enumerate(boxes.items()):
    left, right = key
    enter = False
    for iidx, circuit in enumerate(circuits):
        if left in circuit:
            enter = True
            circuits[iidx].add(right)
        elif right in circuit:
            enter = True
            circuits[iidx].add(left)

    # merge circuits if needed
    to_remove = set()
    for c1, c2 in combinations(circuits, 2):
        inter = len(c1.intersection(c2)) > 0  # same as len(c2.intersection(c1)) > 0
        if inter:  # c1 vs c2 order does not matter
            # merge on c1
            c1_idx = circuits.index(c1)
            circuits[c1_idx].update(c2)

            # add c2 to removal set
            c2_idx = circuits.index(c2)
            to_remove.add(c2_idx)

    for circuit_idx in to_remove:
        circuits.pop(circuit_idx)

    # mutually exclusive, add new circuit
    if not enter:
        circuits.append({left, right})

    for circuit in circuits:
        if len(circuit) == len(arr):
            last_junction = key
            break

    if last_junction:
        break

print(f'Advent of Code Day 8 Answer Part 2: {last_junction[0][0] * last_junction[1][0]}')
