import sys
import copy
from collections import defaultdict
import math
sys.setrecursionlimit(1073741824)
from uuid import uuid4

ZERO = "0"
ONE = "1"
DOT = "."
STAR = "*"
HASH = "#"
DASH = "-"
EQUAL = "="
FULL = 80
HALF = 40
QUARTER = 20
TINY = 10

def b(text):
    return f"\033[94m{text}\033[0m"

def g(text):
    return f"\033[92m{text}\033[0m"

def r(text):
    return f"\033[91m{text}\033[0m"

def lead_zero(num, num_digits = 2):
    zeroes = num_digits - len(str(num))
    return f"{'0' * zeroes}{num}" if zeroes >= 0 else f"{num}"

def rpad(text, length = 5):
    text = str(text)
    spaces = length - len(text)
    return f"{text}{' ' * spaces if spaces > 0 else ''}"

def lpad(text, length = 5):
    text = str(text)
    spaces = length - len(text)
    return f"{' ' * spaces if spaces > 0 else ''}{text}"

def id(num):
    return b(rpad(f"{num}:", 12))

def print_divider(divider=EQUAL, length=FULL):
    print(divider*length)

def exit():
    print("Exiting...")
    sys.exit()

if len(sys.argv) < 2:
    print("Please specify input file.")
    exit()

if sys.argv[1] not in ["input", "input_test"]:
    print("Invalid input file provided. Should be one of ", b("input "),
              "or ", b("input_test"))
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

ROWS = 103
COLS = 101
COLS_HALF = COLS // 2
ROWS_HALF = ROWS // 2

points = []
def get_inputs():
    with open(sys.argv[1], "r") as f:
        for row in f.readlines():
            points.append([list(map(int, p.strip()[2:].split(','))) for p in row.strip().split()][::-1])
            print(points[-1])

print_divider()
inputs = get_inputs()

grid = [[0] * cols] * rows
for iteration in range(1, 101):
    for p in points:
        old_point = p[-1]
        new_point = []

        for i in [0, 1]:
            threshold = ROWS if i else COLS
            # last element of list will be prev iteration, index 0 is velocity
            tmp = old_point[i] + p[0][i]
            if tmp < 0:
                tmp += threshold
            if tmp >= threshold:
                tmp -= threshold
            new_point.append(tmp)

        p.append(new_point)
        grid[new_point[1]][new_point[0]] += 1
        grid[old_point[1]][old_point[0]] -= 1

for row in grid:
    print(row)

q1 = 0 # col < COLS_HALF and row < ROWS_HALF
q2 = 0 # col > COLS_HALF and row < ROWS_HALF
q3 = 0 # col < COLS_HALF and row > ROWS_HALF
q4 = 0 # col > COLS_HALF and row > ROWS_HALF
for p in points:
    col, row = p[-1]
    if col == COLS_HALF:
        continue
    if row == ROWS_HALF:
        continue
    if col < COLS_HALF and row < ROWS_HALF:
        q1 += 1
    if col > COLS_HALF and row < ROWS_HALF:
        q2 += 1
    if col < COLS_HALF and row > ROWS_HALF:
        q3 += 1
    if col > COLS_HALF and row > ROWS_HALF:
        q4 += 1

print(f"q1: {q1}")
print(f"q2: {q2}")
print(f"q3: {q3}")
print(f"q4: {q4}")

print(f"Safety Factor: {q1 * q2 * q3 * q4}")
