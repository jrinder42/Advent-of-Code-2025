"""

Advent of Code 2025 - Day 7

"""

from collections import deque
import numpy as np


arr = []
with open("day07.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        arr.append([char for char in line])

arr = np.array(arr)

# Part 1

start_s = []
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        if arr[i, j] == 'S':
            start_s = [i, j]
            # useless to break here given python scopes, rust would be nice here

last_row = arr.shape[0] - 1
beams = deque([start_s])
splits = 0
while beams:
    current_beam = beams.popleft()
    if current_beam[0] + 1 == last_row:  # last row of grid
        continue

    r, c = current_beam[0] + 1, current_beam[1]
    if arr[r, c] == ".":  # clear path down
        beams.append([r, c])
    elif arr[r, c] == "^":  # split
        # test left split
        if c - 1 < 0:
            continue

        c -= 1
        if [r, c] not in beams:
            beams.append([r, c])

        # test right split
        if c + 1 > arr.shape[1] - 1:
            continue

        c += 2
        if [r, c] not in beams:
            beams.append([r, c])
            splits += 1

print(f'Advent of Code Day 7 Answer Part 1: {splits}')

# Part 2

print(f'Advent of Code Day 7 Answer Part 2: {1}')
