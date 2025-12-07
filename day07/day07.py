"""

Advent of Code 2025 - Day 7

"""

from collections import deque, defaultdict
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
            start_s = (i, j)
            # useless to break here given python scopes, rust would be nice here

last_row = arr.shape[0] - 1
beams = deque([start_s])
splits = 0
while beams:
    current_beam = beams.popleft()
    if current_beam[0] + 1 > last_row:  # last row of grid
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

# any real dfs/bfs algo will be too slow / explode memory-wise (see graph.py)

"""
Explanation as it can be a bit confusing:

1. Find all splitters in a given row
2. For each splitter, move the value from above the splitter into each of the left and right positions below it
3. For each non-splitter, move the value from above into the same position below
    3.5. This is tricky as we need to copy the original dict entering this row as we modify it in-transit
4. Repeat for all rows

Other tricky bit:
    - Sometimes we need to move values, sometimes we need to add values (if two beams converge on one position)
"""

def get_splits(arr, row_idx):
    moves = set()
    for col in range(arr.shape[1]):
        if arr[row_idx, col] == "^":
            moves.add(col)

    return moves

index_list = defaultdict(int)
index_list[start_s[1]] = 1
total = 0
for i in range(1, arr.shape[0]):
    splits = get_splits(arr, i)
    non_splits = set(range(arr.shape[1])) - splits
    additions = {}

    before_dict = index_list.copy()
    for split in splits:
        if additions.get(split - 1, False):
            index_list[split - 1] += index_list[split]
        else:
            index_list[split - 1] = index_list[split]
            additions[split - 1] = True

        if additions.get(split + 1, False):
            index_list[split + 1] += index_list[split]
        else:
            index_list[split + 1] = index_list[split]
            additions[split + 1] = True

        index_list[split] = 0

    for non_split in non_splits:
        if additions.get(non_split, False):
            index_list[non_split] += before_dict[non_split]
        else:
            index_list[non_split] = before_dict[non_split]
            additions[non_split] = True

    index_list = dict(sorted(index_list.items(), key=lambda item: item[0]))

print(f'Advent of Code Day 7 Answer Part 2: {sum(index_list.values())}')

