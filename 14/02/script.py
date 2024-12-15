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
ROWS_HALF = ROWS // 2
COLS_HALF = COLS // 2

points = []
grid = []
for i in range(ROWS):
    grid.append([0] * COLS)

def print_grid():
    for row in grid:
        print(''.join([g(col) if col > 0 else " " for col in row]))

print_grid()
def get_inputs():
    with open(sys.argv[1], "r") as f:
        for row in f.readlines():
            points.append([list(map(int, p.strip()[2:].split(','))) for p in row.strip().split()][::-1])
            col, row = points[-1][-1]
            grid[row][col] += 1

print_divider()
get_inputs()
print(len(points))

connected_sum = 0
visited = set()
def get_neighbor_count(point):
    global connected_sum
    global visited
    if tuple(point) in visited:
        return

    col, row = point
    val = grid[row][col]
    if val == 0:
        return

    connected_sum += grid[row][col]
    visited.add(tuple(point))

    for row_delta, col_delta in [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1],
        [1, 1],
        [1, -1],
        [-1, 1],
        [-1, -1],
    ]:
        new_row, new_col = row + row_delta, col + col_delta
        if new_row < 0 or new_col < 0 or new_row >= ROWS or new_col >= COLS:
            continue
        get_neighbor_count([new_col, new_row])

iteration = 0
max_connected_sum = 0
while True:
    iteration += 1
    print(f"Iteration: {iteration}")
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

    print_grid()
    connected_sum = 0
    visited = set()
    get_neighbor_count(points[0][-1])
    if connected_sum > max_connected_sum:
        max_connected_sum = connected_sum
        print(f"iteration: {iteration}")
        print(f"connected_sum: {connected_sum}")
        input()

# Ok this just happened to work but tbh that's because I got lucky, there's the
# chance that the point I picked to follow with the flood fill could have been
# not one of the right ones.
# other approaches would have been to calculate the min entropy at each frame,
# or to use the chinese remainder theorem because there are only going to be 103
# * 101 distinct positions
