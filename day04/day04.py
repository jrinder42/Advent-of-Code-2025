"""

Advent of Code 2025 - Day 4

"""

from ast import literal_eval

import numpy as np


arr = []
with open("day04.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        arr.append([char for char in line])

arr = np.array(arr)

# Part 1

def spots(point, grid):
    for i in range(-1, 2):
        for j in range(-1, 2):
            r, c = point[0] + i, point[1] + j
            # outside the grid
            if r < 0 or c < 0 or r >= grid.shape[0] or c >= grid.shape[1]:
                continue

            if (r, c) == point:
                continue

            yield grid[r, c], (r, c)

rolls_of_paper = 0
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        val = arr[i, j]
        if val != "@":
            continue

        count = 0
        for spot_val, (r, c) in spots((i, j), arr):
            if spot_val == "@":
                count += 1

        if count < 4:
            rolls_of_paper += 1

print(f'Advent of Code Day 4 Answer Part 1: {rolls_of_paper}')

# Part 2

removal_steps = 0
while True:
    rolls_of_paper = 0
    to_change = []
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            val = arr[i, j]
            if val != "@":
                continue

            count = 0
            for spot_val, (r, c) in spots((i, j), arr):
                if spot_val == "@":
                    count += 1

            if count < 4:
                to_change.append((i, j))
                rolls_of_paper += 1

    if not to_change:
        break

    for r, c in to_change:
        removal_steps += 1
        arr[r, c] = "."

print(f'Advent of Code Day 4 Answer Part 2: {removal_steps}')
