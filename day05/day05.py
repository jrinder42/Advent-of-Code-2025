"""

Advent of Code 2025 - Day 5

"""

from ast import literal_eval


with open("day05.txt", "r") as file:
    fresh_id_ranges, ingredient_ids = file.read().split("\n\n")

fresh_id_ranges = fresh_id_ranges.split("\n")
ingredient_ids = ingredient_ids.split("\n")
ingredient_ids = [literal_eval(num) for num in ingredient_ids]

# Part 1

fresh_ranges = []
for fresh_id_range in fresh_id_ranges:
    left, right = fresh_id_range.split("-")
    left, right = literal_eval(left), literal_eval(right)
    fresh_ranges += [range(left, right + 1)]

count = 0
for ingredient_id in ingredient_ids:
    for fresh_range in fresh_ranges:
        if ingredient_id in fresh_range:
            count += 1
            break

print(f'Advent of Code Day 5 Answer Part 1: {count}')

# Part 2

print(f'Advent of Code Day 5 Answer Part 2: {1}')
