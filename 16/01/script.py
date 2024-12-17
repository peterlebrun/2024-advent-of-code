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
    return f"\033[94;1;4m{text}\033[0m"

def g(text):
    return f"\033[92;1;4m{text}\033[0m"

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
NORTH = "NORTH"
EAST = "EAST"
SOUTH = "SOUTH"
WEST = "WEST"
DELTAS = {
    NORTH: [-1, 0],
    EAST: [0, 1],
    SOUTH: [1, 0],
    WEST: [0, -1],
}
OPPOSITE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}

def print_grid(grid, coords, neighbors, missing_vals=[]):
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
    print(bottom)
    for row_index, row in enumerate(grid):
        output = ""
        for col_index, col in enumerate(row):
            if (row_index, col_index) == coords:
                output += f"{g(col)}"
            elif (row_index, col_index) in neighbors:
                output += f"{b(col)}"
            elif col == WALL:
                output += "\033[37;2m#\033[0m"
            elif (row_index, col_index) in missing_vals:
                output += f"\033[91;1;4m{col}\033[0m"
            else:
                output += f"\033[32;1m{col}\033[0m"
        print(f"{lpad(row_index, 3)}: {output}")

def get_neighbors(grid, row, col, direction):
    neighbors = []
    for ndirection, delta in DELTAS.items():
        next_row, next_col = row + delta[0], col + delta[1]
        if grid[next_row][next_col] == WALL:
            continue
        if direction != ndirection:
            neighbors.append(((row, col, ndirection), 1000))
            continue
        neighbors.append(((next_row, next_col, ndirection), 1))
    return neighbors

grid = []
start_coords = None, None
end_coords = None, None
nodes = []
with open(sys.argv[1], "r") as f:
    for row_index, row in enumerate(f.readlines()):
        row = row.strip()
        grid.append([])
        for col_index, col in enumerate(row):
            if col in [START, EMPTY, END]:
                coords = (row_index, col_index)
                nodes.append(coords)
                if col == START:
                    start_coords = coords
                elif col == END:
                    end_coords = coords
            grid[-1].append(col)

dist = {}
prev = {}
unvisited_nodes = [(*start_coords, EAST)]
visited_nodes = set()
dist[(*start_coords, EAST)] = 0
end_nodes = set()
while len(unvisited_nodes):
    unvisited_nodes.sort(key=lambda u: dist[u])
    node = unvisited_nodes.pop(0)
    visited_nodes.add(node)

    for neighbor, cost in get_neighbors(grid, *node):
        if neighbor in visited_nodes:
            continue
        if (neighbor[0], neighbor[1]) == end_coords:
            end_nodes.add(neighbor)
        elif neighbor not in unvisited_nodes:
            unvisited_nodes.append(neighbor)
        if neighbor not in dist:
            dist[neighbor] = float('inf')
        if neighbor not in prev:
            prev[neighbor] = None

        tmp = dist[node] + cost

        if tmp < dist[neighbor]:
            dist[neighbor] = tmp
            prev[neighbor] = node

for row in grid:
    print(row)

for e in end_nodes:
    print(f"{e}: {dist[e]}")
    print(f"prev: {prev[e]}")
