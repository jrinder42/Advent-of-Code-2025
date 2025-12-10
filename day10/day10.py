"""

Advent of Code 2025 - Day 10

"""

from ast import literal_eval
import numpy as np
from itertools import product
import re
from ortools.sat.python import cp_model


machines = []
with open("day10.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        line_split = line.split()

        light_diagram = line_split[0]
        joltage = line_split[-1]
        wiring_schematics = line_split[1:-1]
        machines.append(
            {
                "light_diagram": light_diagram,
                "wiring_schematics": [elem for elem in wiring_schematics],
                "joltage": [literal_eval(elem) for elem in re.findall(r'\d+', joltage)],
            }
        )

# Part 1

"""
Key Insight:

Because the problem models toggles (pressing a button flips a light), addition is XOR: pressing twice cancels. 
If you try to do regular gaussian elimination without reducing modulo 2, you get:
    - incorrect results
    - negative results
    - or no results

After some googling, this is the same as a Galois Field GF(2) linear algebra problem.
"""

def _parse_light_diagram(diagram):
    grams = []
    for char in diagram:
        if char in ["[", "]"]:
            continue

        if char == ".":
            grams.append(0)
        else:  # char == "#"
            grams.append(1)

    return np.array(grams)

def _parse_buttons(buttons, size):
    parsed_buttons = []
    for button in buttons:
        nums = re.findall(r'\d+', button)
        nums = sorted([literal_eval(num) for num in nums])
        parsed_buttons.append([1 if idx in nums else 0 for idx in range(size)])

    return np.array(parsed_buttons)

def build_system(diagram, buttons):
    gram = _parse_light_diagram(diagram)
    size = len(gram)
    parsed_buttons = _parse_buttons(buttons, size).T  # transpose to get correct shape

    return parsed_buttons, gram


total = 0
for machine in machines:
    A, b = build_system(machine["light_diagram"], machine["wiring_schematics"])

    min_presses = None
    # 0, 1 for every button (press or not)
    # brute force iterate over every combination
    for bits in product([0, 1], repeat=len(machine["wiring_schematics"])):
        x = np.array(bits, dtype=int)
        if np.array_equal((A @ x) % 2, b % 2):
            if min_presses is None or sum(x) < min_presses:
                min_presses = sum(x)

    total += min_presses

print(f'Advent of Code Day 10 Answer Part 1: {total}')

# Part 2

# ILP (Integer Linear Programming) solver, effectively my original idea for Part 1 that I couldn't get working

def build_system_v2(jolts, buttons):
    jolt = np.array(jolts, dtype=int)
    size = len(jolt)
    parsed_buttons = _parse_buttons(buttons, size).T  # transpose to get correct shape

    return parsed_buttons, jolt

def solve(A, b):
    A = np.array(A)
    b = np.array(b)
    n, m = A.shape

    model = cp_model.CpModel()

    # integer decision vars: x_i >= 0
    x = [model.NewIntVar(0, 10**9, f"x{i}") for i in range(m)]

    # add equality constraints A @ x = b
    for i in range(n):
        model.Add(sum(A[i, j] * x[j] for j in range(m)) == b[i])

    model.Minimize(sum(x))  # minimize total presses

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5  # to be safe, set a time limit

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = np.array([solver.Value(var) for var in x], dtype=int)
        return solution

    return None

total = 0
for machine in machines:
    A, b = build_system_v2(machine["joltage"], machine["wiring_schematics"])

    solution = solve(A, b)
    total += sum(solution)

print(f'Advent of Code Day 10 Answer Part 2: {total}')
