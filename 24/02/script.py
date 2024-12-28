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
mapping = {}
rev_mapping = {}
siblings = {}
swaps = {}
z_vals = {}
x_input = 0b0
y_input = 0b0
raw_inputs = []
with open(sys.argv[1], "r") as f:
    for row in f.readlines():
        row = row.strip()
        if row.find(":") != -1:
            key, val = row.split(": ")
            val = int(val)
            vals[key] = val
            if key.startswith(x):
                x_input += (val << int(key[1:]))
            elif key.startswith(y):
                y_input += (val << int(key[1:]))

        if row.find("->") != -1:
            left, right = row.split(" -> ")
            l1, op, l2 = left.split()
            first, second = sorted([l1, l2])
            left = (first, op, second)
            mapping[left] = right
            rev_mapping[right] = left
            if right.startswith(z):
                z_vals[right] = None

for instr in sorted(mapping):
    print(instr, "->", mapping[instr])
input()

xy_output = x_input + y_input
and_output = x_input & y_input
xor_output = x_input ^ y_input

counter = 0
while any([elem is None for elem in z_vals.values()]):
    print(f"Loop {counter}")
    counter += 1

    for (l1, op, l2), right in mapping.items():
        if l1 not in vals or l2 not in vals:
            continue

        # vals[right] means it's already been evaluated
        # not vals[l1|l2] means there isn't enough info to evaluate yet
        if right in vals: continue

        if op == "XOR":
            vals[right] = vals[l1]^vals[l2]
        elif op == "AND":
            vals[right] = vals[l1]&vals[l2]
        elif op == "OR":
            vals[right] = vals[l1]|vals[l2]

        if right.startswith(z):
            z_vals[right] = vals[right]
        print(f"After: {l1, vals[l1], op, l2, vals[l2], right, vals[right]}")

def get_prev(elem, root):
    inputs = rev_mapping[elem]
    root[elem] = []

    if inputs[0].startswith(x) or inputs[0].startswith(y):
        root[elem].append({ inputs: None })
        return

    tmp0 = {}
    tmp2 = {}
    root[elem].append(tmp0)
    root[elem].append({inputs[1]: None})
    root[elem].append(tmp2)
    get_prev(inputs[0], tmp0)
    get_prev(inputs[2], tmp2)

def print_node(node, depth=0):
    pad = "-" * depth + ("> " if depth else "")
    for key, children in node.items():
        if key in ["XOR", "OR", "AND"]:
            print(f"{pad}{key}")
        elif len(children) == 1 and not list(children[0].values())[0]:
            print(f"{pad}{key} {list(children[0].keys())[0]}")
        else:
            print(f"{pad}{key}")
            for elem in node[key]:
                print_node(elem, depth+1)

print_divider(DOT, HALF)
for elem in sorted(z_vals):
    root = {elem: []}
    get_prev(elem, root)
    #print(root)
    print_node(root)
    input()

z_output = 0
for elem in sorted(z_vals):
    val = z_vals[elem]
    z_output += (val << int(elem[1:]))

print(x_input, "", bin(x_input))
print(y_input, "", bin(y_input))
print(and_output, bin(and_output))
print(xor_output, bin(xor_output))
print(xy_output, bin(xy_output))
print(z_output, bin(z_output))
