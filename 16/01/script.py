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

if not sys.argv[1].startswith("input"):
    print("Invalid input file provided.")
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

START = "S"
END = "E"
WALL = "#"
EMPTY = "."
def get_inputs():
    inputs = []
    start_coords = None, None
    with open(sys.argv[1], "r") as f:
        for row_index, row in enumerate(f.readlines()):
            if START in row:
                start_coords = row_index, row.index(START)
            inputs.append([c for c in row.strip()])
    return inputs, start_coords

def print_grid(grid, coords, neighbors):
    top = " " * 5
    bottom = " " * 5
    if len(grid[0]) > 100:
        print("UPDATE PRINT GRID FUNCTION")
        sys.exit()
    for i in range(len(grid[0])):
        if i < 10:
            top += "  "
            bottom += f"{i} "
            continue
        else:
            i = str(i)
            top += f"{i[0]} "
            bottom += f"{i[1]} "
    print(top)
    print(bottom)
    for row_index, row in enumerate(grid):
        output = ""
        for col_index, col in enumerate(row):
            if (row_index, col_index) == coords:
                output += f"{g(col)} "
            elif (row_index, col_index) in neighbors:
                output += f"{b(col)} "
            else:
                output += f"{col} "
        print(f"{lpad(row_index, 3)}: {output}")

def traverse(grid, row, col, parent, node, visited):
    if (row, col) in visited:
        return
    visited.add((row, col))

    neighbors = []
    terminal = None
    for r_delta, c_delta in [
        [-1,  0],
        [ 0,  1],
        [ 1,  0],
        [ 0, -1],
    ]:
        next_row, next_col = row + r_delta, col + c_delta
        if (next_row, next_col) in visited:
            continue
        next_val = grid[next_row][next_col]
        if next_val == END:
            terminal = (next_row, next_col)
            break
        if next_val == WALL:
            continue
        if next_val == EMPTY:
            neighbors.append((next_row, next_col))

    print_divider(DOT, HALF)
    print()
    print_grid(grid, (row, col), neighbors)
    print(f"Traversing ({row},{col})")
    print(f"Neighbors: {neighbors}")
    print(f"Parent: {parent}")
    print(f"Node: {node}")
    print(f"Visited: {visited}")
    input()

    if terminal:
        node[terminal] = END
        return
    if not len(neighbors):
        return
    if len(neighbors) > 1:
        for n in neighbors:
            node[n] = {}
            traverse(grid, n[0], n[1], (row, col), node[n], visited)
    else:
        traverse(grid, neighbors[0][0], neighbors[0][1], parent, node, visited)

grid, start_coords = get_inputs()


print_divider()
print_grid(grid, start_coords, [])
print_divider(DASH, HALF)
print(f"Starting Coords: {start_coords}")
print_divider(DOT, QUARTER)

paths = {}
visited = set()
traverse(grid, start_coords[0], start_coords[1], start_coords, paths, visited)

print_divider(DOT, HALF)
for k, v in paths.items():
    print(f"{k}: {v}")
