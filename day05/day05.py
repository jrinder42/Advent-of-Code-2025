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

all_fresh = []
for fresh_id_range in fresh_id_ranges:
    left, right = fresh_id_range.split("-")
    left, right = literal_eval(left), literal_eval(right)
    if all_fresh:
        count = 0
        for idx, elem in enumerate(all_fresh):
            if elem[0] <= left <= elem[1]:
                elem[1] = max(elem[1], right)
                count += 1
            elif elem[0] <= right <= elem[1]:
                elem[0] = min(elem[0], left)
                count += 1
        if count == 0:  # mutually exclusive ranges
            all_fresh.append([left, right])
    else:
        all_fresh.append([left, right])  # inclusive ranges as the question states

# final step to merge any overlapping ranges
all_fresh = sorted(all_fresh, key=lambda x: x[0])

final_fresh = [all_fresh[0]]
for elem in all_fresh[1:]:
    left, right = final_fresh[-1]
    if elem[0] <= left <= elem[1] and elem[0] <= right <= elem[1]:  # fully contained
        continue

    if left <= elem[0] <= right:
        final_fresh[-1][1] = max(right, elem[1])
    elif left <= elem[1] <= right:
        final_fresh[-1][1] = min(elem[1], right)
    else:  # mutually exclusive
        final_fresh.append(elem)

fresh_ingredients = 0
for left, right in final_fresh:
    fresh_ingredients += (right - left + 1)

print(f'Advent of Code Day 5 Answer Part 2: {fresh_ingredients}')
