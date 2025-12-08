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
    return math.sqrt((p1[0] - p2[0])** 2 + (p1[1] - p2[1])** 2 + (p1[2] - p2[2])** 2)

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

print(f'Advent of Code Day 8 Answer Part 2: {1}')
