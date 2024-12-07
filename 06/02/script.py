import sys
import copy
from collections import defaultdict
sys.setrecursionlimit(1073741824)

INPUT = "input_test" if len(sys.argv) > 1 and sys.argv[1] == "--test" else "input"

START = "START"
END = "END"
EXITS = "EXITS"
CYCLES = "CYCLES"

N = "N"
E = "E"
S = "S"
W = "W"

HASH = "#"
DOT = "."
CARET = "^"

DIRS = {
    N: E,
    E: S,
    S: W,
    W: N
}

VECS = {
    N: (-1,  0),
    E: ( 0,  1),
    S: ( 1,  0),
    W: ( 0, -1),
}

STARTING_DIRECTION = N
STARTING_COORDS = None
grid = []

def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])

def print_divider():
    print("\n")
    print("="*80)

def print_grid():
    print_divider()
    for row in grid:
        print(row)

row_counter = 0
with open(INPUT, 'r') as f:
    for row in f.readlines():
        if CARET in row:
            STARTING_COORDS = (row_counter, row.find(CARET))
        grid.append([c for c in row.strip()])
        row_counter += 1

def get_cell(coords):
    r, c = coords

    if (r < 0 or
        c < 0 or
        r == len(grid) or
        c == len(grid[r])):
        return None

    return grid[r][c]

def traverse(
    coords = STARTING_COORDS,
    direction = STARTING_DIRECTION,
    visited_coords = {},
):
    cell = get_cell(coords)
    next_coords = plus(coords, VECS[direction])
    next_cell = get_cell(next_coords)
    prev = (coords, direction, cell)

    if not next_cell:
        visited_coords[prev] = (END, direction, None)
        return EXITS, copy.deepcopy(visited_coords)

    visited_coords[prev] = (next_coords, direction, next_cell)

    if (next_coords, direction, next_cell) in visited_coords:
        return CYCLES, copy.deepcopy(visited_coords)
    if next_cell == HASH:

        # for hash - don't change direction or update coords
        return traverse(coords, DIRS[direction], visited_coords)

    return traverse(next_coords, direction, visited_coords)

_, visited = traverse()

obstacles = set()
counter = 1
for coords, _, original_cell in visited.values():
    if coords == END or original_cell == HASH or coords in obstacles:
        continue

    row, col = coords
    grid[row][col] = HASH

    result, _ = traverse(STARTING_COORDS, STARTING_DIRECTION, {})
    print(f"{counter}: {coords}\t{result}")
    if result == CYCLES:
        obstacles.add(coords)

    grid[row][col] = original_cell
    counter += 1

print(f"Visited Cells: {len(set([c for (c, _, _) in visited]))}")
print(f"Obstacles: {len(obstacles)}")
