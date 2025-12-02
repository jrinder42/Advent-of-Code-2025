"""

Advent of Code 2025 - Day 2

"""

from ast import literal_eval


lines = []
with open("day02.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        lines += [elem for elem in line.split(',') if elem.strip()]

# Part 1

invalid_ids = []
for idx, line in enumerate(lines):
    left, right = line.split('-')
    left, right = literal_eval(left), literal_eval(right)
    for num in range(left, right + 1):
        str_num = str(num)
        n = len(str_num)
        if len(str_num) % 2 == 0 and str_num[:n // 2] == str_num[n // 2:]:
            invalid_ids += [num]

print(f'Advent of Code Day 2 Answer Part 1: {sum(invalid_ids)}')

# Part 2

def generate_combinations(num_str):
    number = num_str
    n = len(number) // 2

    while n > 0:
        base = num_str[:n]
        count = 0
        for i in range(n, len(num_str), n):
            elem = num_str[i:i + n]
            if elem != base:
                count += 1

        if count == 0:
            return True, base

        n -= 1

    return False, num_str

invalid_ids = []
for idx, line in enumerate(lines):
    left, right = line.split('-')
    left, right = literal_eval(left), literal_eval(right)
    for num in range(left, right + 1):
        str_num = str(num)

        is_good, _ = generate_combinations(str_num)
        if is_good:
            invalid_ids += [num]

print(f'Advent of Code Day 2 Answer Part 2: {sum(invalid_ids)}')
