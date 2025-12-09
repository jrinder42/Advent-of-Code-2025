"""

Advent of Code 2025 - Day 9

"""

from ast import literal_eval
from itertools import combinations
import numpy as np


pairs = []
with open("day09.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        pairs.append([literal_eval(num) for num in line.split(",")])

# swap
for idx, pair in enumerate(pairs):
    r, c = pair
    pairs[idx] = [c, r]

large_r, large_c = None, None
for r, c in pairs:
    if large_r is None or r > large_r:
        large_r = r
    if large_c is None or c > large_c:
        large_c = c

large_r, large_c = max(large_r, large_c), max(large_r, large_c)
grid = np.full((large_r + 1, large_c + 1), ".")

for r, c in pairs:
    grid[r][c] = "#"

# Part 1

largest = [None, None]
for combination in combinations(pairs, 2):
    left, right = sorted(combination, key=lambda x: (x[0], x[1]))
    dr = right[0] - left[0] + 1
    dc = right[1] - left[1] + 1

    area = dr * dc

    if largest[0] is None or largest[0] < area:
        largest = [area, combination]

print(f'Advent of Code Day 9 Answer Part 1: {largest[0]}')

# Part 2

print(f'Advent of Code Day 9 Answer Part 2: {1}')

