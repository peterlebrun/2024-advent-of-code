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
ROW_MAX_INDEX = ROWS - 1
COL_MAX_INDEX = COLS - 1
class Point:
    def __init__(self, coords, velocity):
        self.pid = str(uuid4())
        self.row_original = coords[1]
        self.col_original = coords[0]
        self.row_velocity = int(velocity[1])
        self.col_velocity = int(velocity[0])
        self.age = 0

    def increment(self):
        self.age += 1

    def get_row(self):
        return (self.row_original + self.age * self.row_velocity) % ROW_MAX_INDEX

    def get_col(self):
        return (self.col_original + self.age * self.col_velocity) % COL_MAX_INDEX

    def __repr__(self):
        return id(self.pid) + g(f" ({self.get_row()},{self.get_col()}): ") + g(f"({self.row_velocity}, {self.col_velocity})")
        return "\n".join([
            r("-" * 50),
            b("Point ") + id(self.pid),
            b("Age: ") + g(self.age),
            b("Original Coords: ") + g(f"({self.row_original}, {self.col_original})"),
            b("Current Coords: ") + g(f"({self.get_row()}, {self.get_col()})"),
            b("Velocity: ") + g(f"({self.row_velocity}, {self.col_velocity})"),
        ])

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None] * cols] * rows
        self.age = 0

    def add(self, point):
        row, col = point.get_row(), point.get_col()

        if not self.grid[row][col]:
            self.grid[row][col] = {}

        print(f"Adding point to ({row}, {col})")
        self.grid[row][col][point.pid] = point

    def iterate(self):
        self.age += 1
        for row in range(self.rows):
            for col in range(self.cols):
                for point in grid[row][col].items():
                    if point.age < self.age:
                        point.increment()
                        self.add(point)
                        del self.grid[row][col][point.pid]

points = []
def get_inputs():
    with open(sys.argv[1], "r") as f:
        for row in f.readlines():
            points.append([list(map(int, p.strip()[2:].split(','))) for p in row.strip().split()][::-1])
            print(points[-1])

print_divider()
inputs = get_inputs()

for iteration in range(1, 101):
    print_divider(DASH, HALF)
    for p in points:
        new_point = []
        for i in [0, 1]:
            threshold = ROWS if i else COLS
            # last element of list will be prev iteration, index 0 is velocity
            tmp = p[-1][i] + p[0][i]
            if tmp < 0:
                tmp += threshold
            if tmp >= threshold:
                tmp -= threshold
            new_point.append(tmp)
        p.append(new_point)

COLS_HALF = COLS // 2
ROWS_HALF = ROWS // 2

q1 = 0 # col < COLS_HALF and row < ROWS_HALF
q2 = 0 # col > COLS_HALF and row < ROWS_HALF
q3 = 0 # col < COLS_HALF and row > ROWS_HALF
q4 = 0 # col > COLS_HALF and row > ROWS_HALF
for p in points:
    col, row = p[-1]
    if col == COLS_HALF:
        continue
    if row == ROWS_HALF:
        continue
    if col < COLS_HALF and row < ROWS_HALF:
        q1 += 1
    if col > COLS_HALF and row < ROWS_HALF:
        q2 += 1
    if col < COLS_HALF and row > ROWS_HALF:
        q3 += 1
    if col > COLS_HALF and row > ROWS_HALF:
        q4 += 1

print(f"q1: {q1}")
print(f"q2: {q2}")
print(f"q3: {q3}")
print(f"q4: {q4}")

print(f"Safety Factor: {q1 * q2 * q3 * q4}")
