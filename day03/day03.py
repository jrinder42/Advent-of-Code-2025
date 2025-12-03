"""

Advent of Code 2025 - Day 3

"""

from ast import literal_eval


lines = []
with open("day03.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        lines.append([literal_eval(num) for num in line])

# Part 1

def find_joltage(num_list):
    large = None

    n = len(num_list)
    for i in range(n):
        for j in range(i + 1, n):
            num = literal_eval(str(num_list[i]) + str(num_list[j]))
            if large is None or num > large:
                large = num

    return large

jolts_list = []
for line in lines:
    jolts = find_joltage(line)
    jolts_list.append(jolts)

print(f'Advent of Code Day 3 Answer Part 1: {sum(jolts_list)}')

# Part 2

def joltage_v2(num_list):
    cap = 12

    if len(num_list) < cap:
        return None

    jolts = []
    start = 0
    for _ in range(cap):
        end = len(num_list) - cap + 1
        top = max(num_list[start:end])

        jolts.append(top)

        idx = num_list.index(top)
        num_list.append(top)  # janky that we need this
        num_list = num_list[idx + 1:]

    return jolts

jolts_list = []
for line in lines:
    jolts = joltage_v2(line)
    jolts_list.append(literal_eval("".join(str(elem) for elem in jolts)))

print(f'Advent of Code Day 3 Answer Part 2: {sum(jolts_list)}')
