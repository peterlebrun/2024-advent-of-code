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

def insert(string, node):
    for key in node:
        if string.startswith(key):
            insert(string, node[key])
            return

        if key.startswith(string):
            node[string] = {key: node[key]}
            del node[key]
            return
    node[string] = {}

def generate_reverse_trie(string, node):
    is_child = False
    for key in node:
        if key.startswith(string):
            is_child = True
            generate_reverse_trie(string, node[key])
    if not is_child:
        node[string] = {}

def print_node(node, depth=0):
    pad = "-" * depth + (">" if depth else "")
    for key in node:
        print(f"{pad}{key}")
        print_node(node[key], depth+1)

def is_possible(row, trie):
    if not(row): return True

    node = trie
    while len(node):
        outer_loop_should_break = True
        for key in node:
            if row.startswith(key):
                if is_possible(row[len(key):], trie):
                    return True
                node = node[key]
                outer_loop_should_break = False
                break

        if outer_loop_should_break:
            break

    return False

accum = []
def get_possibilities(row, trie, possibility=[]):
    global accum
    node = trie
    outer_loop_should_break = False
    while not outer_loop_should_break:
        outer_loop_should_break = True
        for key in node:
            if row == key:
                accum.append([*possibility, key])
                break

            if row.startswith(key):
                get_possibilities(row[len(key):], trie, [*possibility, key])
                node = node[key]
                possibility = possibility.copy()
                outer_loop_should_break = False
                break

trie = {}
atoms = []
molecules = {}
with open(sys.argv[1], "r") as f:
    for index, row in enumerate(f.readlines()):
        row = row.strip()
        if index == 0:
            atoms = row.split(', ')
            atoms.sort(key=len)
            for a in atoms:
                insert(a, trie)
            print_node(trie)

        if index >= 2:
            print(f"Evaluating row {index}: {row}")
            if is_possible(row, trie):
                molecules[row] = []

print(molecules)

for m in molecules:
    for a in atoms:
        if m.find(a) != -1 and m != a:
            molecules[m].append(a)

for parent, children in molecules.items():
    print_divider(DOT, HALF)
    print(id(parent))
    children.sort(key=len, reverse=True)
    for atom in children:
        print(atom)
