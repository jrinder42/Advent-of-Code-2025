"""

Advent of Code 2025 - Day 12

"""

from ast import literal_eval
from typing import NamedTuple
import numpy as np


regions = []
presents = []
with open("day12.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        if "x" in line:
            regions.append(line)
        else:
            presents.append(line)

class Present(NamedTuple):
    id: int
    shape: np.ndarray

class Regions(NamedTuple):
    grid: tuple[int, int]
    present_list: list[int]

# parse regions
new_regions = []
for region in regions:
    left, right = region.split(": ")
    new_regions.append(
        Regions(
            grid=(literal_eval(left.split("x")[0]), literal_eval(left.split("x")[1])),
            present_list=[literal_eval(x) for x in right.split()],
        )
    )

# parse presents
mod_presents = []
inner = []
for present in presents:
    if not present.strip():
        mod_presents.append(inner)
        inner = []
        continue

    inner.append(present)

presents = {}
for mod_present in mod_presents:
    idx = literal_eval(mod_present[0][:-1])
    rest = mod_present[1:]
    shape = [[elem for elem in char] for char in rest]
    presents[idx] = Present(
        id=idx,
        shape=np.array(shape),
    )

# Part 1

present_fit = 0
for new_region in new_regions:
    total = 0
    for idx, freq in enumerate(new_region.present_list):
        p = presents[idx]
        if freq:
            part_of_shape = np.where(p.shape == "#")[0]
            total += freq * p.shape.shape[0] * p.shape.shape[1]

    grid_area = new_region.grid[0] * new_region.grid[1]
    if total <= grid_area:
        present_fit += 1

print(f'Advent of Code Day 12 Answer Part 1: {present_fit}')
