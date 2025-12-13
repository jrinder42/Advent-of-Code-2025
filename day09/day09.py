"""

Advent of Code 2025 - Day 9

"""

from ast import literal_eval
from itertools import combinations
import numpy as np
from shapely.geometry import Polygon, box


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
    grid[r, c] = "#"

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

def largest_rectangle(corners):
    poly = Polygon(corners)

    if not poly.is_valid:
        raise ValueError("The provided corners do not form a valid polygon.")

    candidates = []  # this cannot be a dict because we can have multiple coordinates with the same area

    # We use combinations to get every unique pair of vertices
    for point1, point2 in combinations(corners, 2):
        x1, y1 = point1
        x2, y2 = point2

        # area = 0
        if x1 == x2 or y1 == y2:
            continue

        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        area = width * height

        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        candidate_rectangle = box(min_x, min_y, max_x, max_y)
        candidates.append((area, candidate_rectangle))

    # heuristic to speed up search: sort by area (Largest --> smallest)
    candidates.sort(key=lambda x: x[0], reverse=True)

    for area, rectangle in candidates:
        if poly.contains(rectangle):
            bounds = rectangle.bounds  # (minx, miny, maxx, maxy)
            return area, bounds

    return 0, None

largest, rectangle = largest_rectangle(pairs)

print(f'Advent of Code Day 9 Answer Part 2: {largest}')
