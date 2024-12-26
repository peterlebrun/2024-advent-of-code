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

x = "x"
y = "y"
z = "z"
vals = {}
mapping = defaultdict(list)
rev_mapping = {}
swaps = {}
z_vals = {}
x_input = 0b0
y_input = 0b0
with open(sys.argv[1], "r") as f:
    for row in f.readlines():
        row = row.strip()
        if row.find(":") != -1:
            key, val = row.split(": ")
            val = int(val)
            vals[key] = val
            print(f"Key: {key}, {vals[key]}")
            if key.startswith(x):
                x_input += (val << int(key[1:]))
            elif key.startswith(y):
                y_input += (val << int(key[1:]))

        if row.find("->") != -1:
            left, right = row.split(" -> ")
            left = tuple(left.split())
            print(f"left,right: {left}, {right}")
            mapping[left].append(right)
            rev_mapping[right] = left
            if right.startswith(z):
                z_vals[right] = None

for elem in mapping:
    print(f"Mapping: {elem}, {mapping[elem]}")

for elem in z_vals:
    print(f"{elem}, {z_vals[elem]}")


xy_output = x_input + y_input

counter = 0
while any([elem is None for elem in z_vals.values()]):
    print(f"Loop {counter}")
    counter += 1

    for (l1, op, l2), outputs in mapping.items():
        print_divider(DOT, HALF)
        print(f"Entry: {l1, op, l2, outputs}")
        if l1 not in vals or l2 not in vals:
            print(f"l1/l2 missing")
            continue

        print(f"Before: {vals[l1], vals[l2]}")

        for right in outputs:
        # vals[right] means it's already been evaluated
        # not vals[l1|l2] means there isn't enough info to evaluate yet
            if right in vals:
                print(f"Already Evaluated")
                continue

            if op == "XOR":
                vals[right] = vals[l1]^vals[l2]

            if op == "AND":
                vals[right] = vals[l1]&vals[l2]

            if op == "OR":
                vals[right] = vals[l1]|vals[l2]

            if right.startswith(z):
                z_vals[right] = vals[right]
            print(f"After: {vals[l1], vals[l2], vals[right]}")

z_output = 0
for elem in sorted(z_vals):
    val = z_vals[elem]
    z_output += (val << int(elem[1:]))
    print(elem, val)
    print(z_output)

print(x_input, "", bin(x_input))
print(y_input, "", bin(y_input))
print(xy_output, bin(xy_output))
print(z_output, bin(z_output))
