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
        if ROBOT in row:
            start = (row_index, row.index(ROBOT))
        if WALL in row:
            warehouse.append([col for col in row])
            continue
        instructions += row

def print_warehouse():
    for row in warehouse:
        output = ""
        for col in row:
            if col == ROBOT:
                output += g(col)
            elif col == BOX:
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

def attempt_move(coords, direction):
    row, col = coords[0] + direction[0], coords[1] + direction[1]
    if warehouse[row][col] == WALL:
        return False
    if warehouse[row][col] == EMPTY:
        warehouse[row][col] = warehouse[coords[0]][coords[1]]
        warehouse[coords[0]][coords[1]] = EMPTY
        return True
    if warehouse[row][col] == BOX:
        if attempt_move((row, col), direction):
            warehouse[row][col] = warehouse[coords[0]][coords[1]]
            warehouse[coords[0]][coords[1]] = EMPTY
            return True
        return False

print_divider()
print(f"Start: {id(start)}")
print_warehouse()

coords = start
for index, i in enumerate(instructions):
    print_divider(DASH, HALF)
    direction = DIRS[i]
    print(f"Moving {i}")
    #is_able_to_move, dot_coords = can_move(coords, DIRS[i])
    if attempt_move(coords, DIRS[i]):
        coords = (coords[0] + DIRS[i][0], coords[1] + DIRS[i][1])
    print_warehouse()

gps_sum = 0
for row_index, row in enumerate(warehouse):
    for col_index, col in enumerate(row):
        if col == BOX:
            gps_sum += 100 * row_index + col_index

print(f"GPS Sum: {gps_sum}")
