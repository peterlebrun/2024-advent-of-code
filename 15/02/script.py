import sys
import copy
from collections import defaultdict
import math
from types import new_class
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
    return f"\033[92m{text}\033[0m"

def r(text):
    return f"\033[91;1m{text}\033[0m"

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

if not sys.argv[1].startswith("input"):
    print("Invalid input file provided.")
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"
WALL = "#"
ROBOT = "@"
BOX = "O"
EMPTY = "."
LBOX = "["
RBOX = "]"

DIRS = {
    UP:    (-1,  0),
    DOWN:  ( 1,  0),
    LEFT:  ( 0, -1),
    RIGHT: ( 0,  1),
}

warehouse = []
instructions = ""
start = None, None
with open(sys.argv[1], "r") as f:
    for row_index, row in enumerate(f.readlines()):
        row = row.strip()
        if not len(row):
            continue

        if row.find(UP) > 0 or row.find(DOWN) > 0 or row.find(LEFT) > 0 or row.find(RIGHT) > 0:
            instructions += row
            continue

        warehouse.append([])
        for col_index, col in enumerate(row):
            addend = []
            if col == WALL:
                addend = [WALL, WALL]
            elif col == ROBOT:
                start = row_index, col_index * 2
                addend = [ROBOT, EMPTY]
            elif col == BOX:
                addend = [LBOX, RBOX]
            else:
                addend = [EMPTY, EMPTY]
            warehouse[-1].extend(addend)

def print_warehouse():
    for row in warehouse:
        output = ""
        for col in row:
            if col == ROBOT:
                output += g(col)
            elif col in [LBOX, RBOX]:
                output += r(col)
            else:
                output += col
        print(output)

MAX_INDEX = len(instructions) - 1
TOTAL_LEN = 11
def print_instructions(index):
    if index < TOTAL_LEN:
        pre = instructions[:index]
        post = instructions[index+1:TOTAL_LEN+1]
    elif index == MAX_INDEX:
        pre = instructions[MAX_INDEX - TOTAL_LEN:MAX_INDEX]
        post = ""
    elif index < MAX_INDEX - TOTAL_LEN:
        pre = instructions[index-5:index]
        post = instructions[index + 1:index + 6]
    else:
        pre = instructions[MAX_INDEX - TOTAL_LEN:index]
        post = instructions[index + 1:]

    print(pre, b(instructions[index]), post, sep="")

def attempt_horizontal_move(coords, direction):
    row, col = coords[0] + direction[0], coords[1] + direction[1]
    if warehouse[row][col] == WALL:
        print(row, col, "WALL")
        return False
    if warehouse[row][col] == EMPTY:
        print(row, col, "EMPTY")
        warehouse[row][col] = warehouse[coords[0]][coords[1]]
        warehouse[coords[0]][coords[1]] = EMPTY
        return True
    if warehouse[row][col] in [LBOX, RBOX]:
        print(row, col, "BOX")
        if attempt_horizontal_move((row, col), direction):
            warehouse[row][col] = warehouse[coords[0]][coords[1]]
            warehouse[coords[0]][coords[1]] = EMPTY
            return True
        return False

def evaluate_vertical_move(row, col, direction, parent, transition_map):
    current_val = warehouse[row][col]
    if (row, col) not in transition_map:
        transition_map[(row, col)] = [current_val, EMPTY]
    next_row = row + direction[0]
    next_val = warehouse[next_row][col]
    print(f"Evaluating ({row},{col})-{direction} Current: {current_val}, Next:{next_val}")
    transition_map[(next_row, col)] = [next_val, current_val] # maps to pre, post

    node = {}
    parent[(row, col)] = node
    if next_val == WALL:
        node[(next_row, col)] = WALL
    elif next_val == EMPTY:
        node[(next_row, col)] = EMPTY
    else:
        evaluate_vertical_move(next_row, col, direction, node, transition_map)
        # If we have LBOX or RBOX, make sure we get the other side of the box too
        if next_val == LBOX:
            evaluate_vertical_move(next_row, col + 1, direction, node, transition_map)
        if next_val == RBOX:
            evaluate_vertical_move(next_row, col - 1, direction, node, transition_map)

print_divider()
print(f"Start: {id(start)}")
print_warehouse()

print_divider()
print("PRINTING WAREHOUSE")
for row in warehouse:
    print(row)
print_divider()

coords = start
for index, instruction in enumerate(instructions):
    row, col = coords
    direction = DIRS[instruction]
    print_divider(DASH, HALF)
    print(f"Step {index + 1} Moving {instruction} from ({row},{col})")
    if instruction in [UP, DOWN]:
        tree = {}
        transition_map = {}
        evaluate_vertical_move(row, col, direction, tree, transition_map)
        print(f"Tree: {tree}")
        print(f"Transition: {transition_map}")
        if any([val[0] == WALL for val in transition_map.values()]):
            continue
        for (next_row, next_col), (pre, post) in transition_map.items():
            if pre == post:
                continue
            warehouse[next_row][next_col] = post
        warehouse[row][col] = EMPTY
        coords = (row + direction[0], col + direction[1])
        print_divider(DOT, HALF)

    if instruction in [LEFT, RIGHT]:
        if attempt_horizontal_move(coords, direction):
            coords = (row + direction[0], col + direction[1])
    print_warehouse()

gps_sum = 0
for row_index, row in enumerate(warehouse):
    for col_index, col in enumerate(row):
        if col == LBOX:
            gps_sum += 100 * row_index + col_index

print(f"GPS Sum: {gps_sum}")
