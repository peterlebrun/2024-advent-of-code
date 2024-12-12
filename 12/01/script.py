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
        print(coords, k, row, col)
        if row < 0 or col < 0 or row >= len(inputs) or col >= len(inputs[0]):
            continue
        neighbors[k] = (row, col)

    return neighbors

for row in range(len(inputs)):
    print(inputs[row])

print_divider(DASH, HALF)
regions = defaultdict(dict)
for row in range(len(inputs)):
    for col in range(len(inputs[row])):
        print_divider(DASH, HALF)
        region_id = inputs[row][col]
        coords = (row, col)

        node = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None,
        }

        print(f"{id(coords)}: {region_id}")
        for k, (n_r, n_c) in get_neighbors(coords).items():
            if n_r == None:
                continue
            print(f"Neighbor: {k}: ({n_r}, {n_c})")
            if inputs[n_r][n_c] == region_id:
                node[k] = (n_r, n_c)
        regions[region_id][coords] = node

def get_perimeter(region):
    perimeter = 0
    for direction in [UP, DOWN, LEFT, RIGHT]:
        for plot in region.values():
            perimeter += int(plot[direction] == None)
    return perimeter

def should_add_to_this_group(node, group):
    if len(group) == 0:
        return True

    for direction in [UP, DOWN, LEFT, RIGHT]:
        if node[direction] in group:
            return True

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
        perimeter = get_perimeter(region)
        cost = area * perimeter
        total_cost += cost
        print(f"{id(region_id)} Area: {area} Perimeter: {perimeter} Cost: {cost}")
        for plot, node in region.items():
            print(g(plot), r(node))

print(f"Total Cost: {total_cost}")
