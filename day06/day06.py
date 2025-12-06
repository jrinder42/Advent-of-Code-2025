"""

Advent of Code 2025 - Day 6

"""

from collections import defaultdict


rows = []
with open("day06.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        rows.append([char for char in line.split()])

nums, special = rows[:-1], rows[-1]

n = len(nums[0])
homework = defaultdict(list[int])
for idx, row in enumerate(nums):
    for iidx, num in enumerate(row):
        homework[iidx].append(row[iidx])

total = 0
for idx, (key, value) in enumerate(homework.items()):
    total += eval(f" {special[idx]} ".join(value))

# Part 1

print(f'Advent of Code Day 6 Answer Part 1: {total}')

# Part 2

print(f'Advent of Code Day 6 Answer Part 2: {1}')
