"""

Advent of Code 2025 - Day 1

"""

from ast import literal_eval
from copy import deepcopy

lines = []
with open("day01.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        dir, num = line[0], literal_eval(line[1:])
        lines.append({"dir": dir, "num": num})

# Part 1

start = 50
high = 100
count = 0
for line in lines:
    dir = line["dir"]
    num = line["num"]

    if dir == "L":
        val = high - num
    else:  # R
        val = num

    _, rem = divmod(val, high)
    start += rem
    start %= high

    if start == 0:
        count += 1

print(f'Advent of Code Day 1 Answer Part 1: {count}')

# Part 2

# just count movements that go past 0 in either direction

def countdown_left(num, init_val):
    clicks = 0
    nn = deepcopy(init_val)

    while num > 0:
        init_val -= 1
        if init_val < 0:
            init_val = 99
            clicks += 1

        num -= 1

    if nn == 0:  # if we land on 0, don't count the last click
        clicks -= 1

    return init_val, clicks


def countdown_right(num, init_val):
    clicks = 0

    while num > 0:
        init_val += 1
        if init_val == 100:
            init_val = 0
            clicks += 1

        num -= 1

    if init_val == 0:
        clicks -= 1

    return init_val, clicks

start = 50
count = 0
total_clicks = 0
for line in lines:
    dir = line["dir"]
    num = line["num"]

    if dir == "L":
        start, clicks = countdown_left(num, start)
    else:  # R
        start, clicks = countdown_right(num, start)

    total_clicks += clicks
    if start == 0:
        count += 1

print(f'Advent of Code Day 1 Answer Part 2: {count + total_clicks}')
