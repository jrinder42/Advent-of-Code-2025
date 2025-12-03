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


print(f'Advent of Code Day 3 Answer Part 2: {1}')
