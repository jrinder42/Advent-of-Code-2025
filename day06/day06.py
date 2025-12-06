"""

Advent of Code 2025 - Day 6

"""

from collections import defaultdict


rows = []
raw = []
with open("day06.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        raw.append(line)
        rows.append([char for char in line.split()])

nums, special = rows[:-1], rows[-1]
raw_nums, raw_special = raw[:-1], raw[-1]

n = len(nums[0])
homework = defaultdict(list)
for idx, row in enumerate(nums):
    for iidx, num in enumerate(row):
        homework[iidx].append(row[iidx])

total = 0
for idx, (key, value) in enumerate(homework.items()):
    total += eval(f" {special[idx]} ".join(value))

# Part 1

print(f'Advent of Code Day 6 Answer Part 1: {total}')

# Part 2

# index stuff
start_indexes = []
for idx, char in enumerate(raw_special):
    if char.strip():
        start_indexes.append(idx)

index_ranges = []
for idx, start_index in enumerate(start_indexes[1:], 1):
    index_ranges.append([start_indexes[idx - 1], start_index - 1]) # not inclusive
val_range = [start_indexes[-1], len(raw_special)]
largest = None
for row in raw_nums:
    col = row[val_range[0]:]
    if largest is None or len(col.strip()) > largest:
        largest = len(col.strip())
index_ranges.append([start_indexes[-1], start_indexes[-1] + largest])

# final calculation
total = 0
for index_idx, index_range in enumerate(index_ranges):
    other_math = defaultdict(list)
    new_rows = []
    for idx, row in enumerate(raw_nums):
        col = row[index_range[0]:index_range[1]]

        new_str = ""
        for iidx, char in enumerate(col):
            if not char.strip():
                new_str += "@"
            else:
                new_str += char

        new_rows.append(new_str)

    for new_row in new_rows:
        for iidx, char in enumerate(new_row):
            other_math[iidx].append(char)

    final_val_list = []
    for _, num_list in other_math.items():
        num_hit = False
        val_list = []
        for char in num_list:
            if char.isdigit():
                val_list.append(char)
                num_hit = True
            elif num_hit and char == "@":
                break

        final_val_list.append("".join(val_list))
    total += eval(f" {special[index_idx]} ".join(final_val_list))

print(f'Advent of Code Day 6 Answer Part 2: {total}')
