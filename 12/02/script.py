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
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
COORDS = "COORDS"
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
    spaces = length - len(text)
    return f"{text}{' ' * spaces if spaces > 0 else ''}"

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

def get_inputs():
    with open(sys.argv[1], "r") as f:
        return [r.strip() for r in f.readlines()]

def get_distance(a, b):
    return (a[0]-b[0], a[1]-b[1])

inputs = get_inputs()

def get_neighbors(coords):
    neighbors = {
        UP: (None, None),
        DOWN: (None, None),
        LEFT: (None, None),
        RIGHT: (None, None),
    }

    for k, (diff_r, diff_c) in {
        UP: (-1, 0),
        DOWN: ( 1,  0),
        LEFT: ( 0, -1),
        RIGHT: (0,  1),
    }.items():
        row = coords[0] + diff_r
        col = coords[1] + diff_c
        if row < 0 or col < 0 or row >= len(inputs) or col >= len(inputs[0]):
            continue
        neighbors[k] = (row, col)

    return neighbors

for row in range(len(inputs)):
    print(inputs[row])

regions = defaultdict(dict)
for row in range(len(inputs)):
    for col in range(len(inputs[row])):
        region_id = inputs[row][col]
        coords = (row, col)

        node = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None,
        }

        for k, (n_r, n_c) in get_neighbors(coords).items():
            if n_r == None:
                continue
            if inputs[n_r][n_c] == region_id:
                node[k] = (n_r, n_c)
        regions[region_id][coords] = node

def get_perimeter(region):
    perimeter = 0
    for direction in [UP, DOWN, LEFT, RIGHT]:
        for plot in region.values():
            perimeter += int(plot[direction] == None)
    return perimeter

def get_num_sides(region):
    edges = defaultdict(list)

    # Map direction to whether we want the row or the col to stay constant
    r_c_map = {
        UP: 0,
        DOWN: 0,
        LEFT: 1,
        RIGHT: 1,
    }

    for direction in [UP, DOWN, LEFT, RIGHT]:
        for coords, plot in region.items():
            if plot[direction] == None:
                # if we have direction, row, store all cols in array
                # if we have direction, col, store all rows in array
                edges[(direction, coords[r_c_map[direction]])].append(coords[1-r_c_map[direction]])

    # if all the stored "other axis" coordinates are continuous, that is one side.
    # for every break in continuity, that adds one more side
    count = 0
    for edge, other_axis in edges.items():
        count += 1
        other_axis.sort()
        for i in range(len(other_axis)-1):
            count += int(other_axis[i] + 1 != other_axis[i+1])

    return count

# I can't believe this works lol
def evaluate_neighbors(coords, node, original, accum = {}):
    accum[coords] = node
    del original[coords]
    for direction in [UP, DOWN, LEFT, RIGHT]:
        if node[direction] and node[direction] not in accum:
            evaluate_neighbors(node[direction], original[node[direction]], original, accum)

total_cost = 0
for region_id, plots in regions.items():
    groupings = []
    while len(plots):
        accum = {}
        seed_coords, seed_node = list(plots.items())[0]
        accum[seed_coords] = seed_node
        evaluate_neighbors(seed_coords, seed_node, plots, accum)
        groupings.append(accum)

    for region in groupings:
        print_divider(DOT, QUARTER)
        area = len(region)
        num_sides = get_num_sides(region)
        cost = area * num_sides
        total_cost += cost
        print(f"{id(region_id)} Area: {area} Num Sides: {num_sides} Cost: {cost}")

print(f"Total Cost: {total_cost}")
