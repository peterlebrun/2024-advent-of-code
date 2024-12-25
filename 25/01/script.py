import sys
import copy
from collections import defaultdict
import math
sys.setrecursionlimit(1073741824)

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

def b(text): return f"\033[94m{text}\033[0m"
def g(text): return f"\033[92m{text}\033[0m"
def r(text): return f"\033[91m{text}\033[0m"

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

def id(num, length = 12):
    return b(rpad(f"{num}:", length))

def print_divider(divider=EQUAL, length=FULL):
    print(divider*length)

def print_grid(grid, coords=(None, None), neighbors=set(), missing_vals=[]):
    top = " " * 5
    middle = " " * 5
    bottom = " " * 5
    for i in range(len(grid[0])):
        if i < 10:
            top += " "
            middle += " "
            bottom += f"{i}"
            continue
        elif i < 100:
            i = str(i)
            top += f" "
            middle += f"{i[0]}"
            bottom += f"{i[1]}"
        else:
            i = str(i)
            top += f"{i[0]}"
            middle += f"{i[1]}"
            bottom += f"{i[2]}"
    print(top)
    print(middle)
    print(bottom)
    for row_index, row in enumerate(grid):
        output = ""
        for col_index, col in enumerate(row):
            if (row_index, col_index) == coords:
                output += f"{g(col)}"
            elif (row_index, col_index) in neighbors:
                output += b("0")
            elif col == WALL:
                output += "\033[37;2m#\033[0m"
            elif (row_index, col_index) in missing_vals:
                output += f"\033[91;1;4m{col}\033[0m"
            else:
                output += f"\033[32;1m{col}\033[0m"

        print(f"{lpad(row_index, 3)}: {output}")

def exit():
    print("Exiting...")
    sys.exit()

if len(sys.argv) < 2:
    print("Please specify input file.")
    exit()

if not sys.argv[1].startswith("input"):
    print("Invalid input file provided.")
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

def add(vec1, vec2):
    if len(vec1) != len(vec2):
        print("Vectors not same length.")
        return
    return [vec1[i] + vec2[i] for i in range(len(vec1))]

keys = []
locks = []

will_start = True
is_lock = None
tmp_vec = [0] * 5
tmp_counter = 1
inputs = [[]]
with open(sys.argv[1], "r") as f:
    for row in f.readlines():
        print("Before:", row, is_lock, tmp_counter, tmp_vec)
        row = row.strip()
        if not len(row):
            inputs.append([])
            continue
        inputs[-1].append([1 if c == HASH else 0 for c in row])

for i in inputs:
    print_divider(DOT)
    for row in i:
        print(row)
    is_lock = sum(i[0]) == 5

    tmp = [0] * 5
    if is_lock:
        for j in range(1, 7):
            tmp = add(tmp, i[j])
        locks.append(tmp)
    else:
        for j in range(0, 6):
            tmp = add(tmp, i[j])
        keys.append(tmp)

num_fits = 0
for k in keys:
    for l in locks:
        a = add(k, l)
        print(k, l, a)
        if any([x >= 6 for x in a]):
            continue
        num_fits += 1

print(f"Num fits: {num_fits}")
