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

# this depends on the keys being inserted in a sorted alphabetical order
# otherwise it won't work
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

def print_node(node, depth=0):
    pad = "-" * depth + (">" if depth else "")
    for key in node:
        print(f"{pad}{key}")
        print_node(node[key], depth+1)

memos = defaultdict(int)
def get_possibility_count(row, trie):
    if row in memos: return memos[row]

    node = trie
    should_recurse = True
    while should_recurse:
        should_recurse = False

        for k in node:
            if row.startswith(k):
                # case of row == k means that we have a completed string match -
                # so add 1. Otherwise, traverse and start counting next chunk of string
                memos[row] += 1 if row == k else get_possibility_count(row[len(k):], trie)
                node = node[k]
                should_recurse = True
                break

    return memos[row]


trie = {}
tokens = []
counter = 0
with open(sys.argv[1], "r") as f:
    for index, row in enumerate(f.readlines()):
        row = row.strip()
        if index == 0:
            tokens = row.split(', ')
            tokens.sort(key=len)
            for t in tokens:
                insert(t, trie)

        if index >= 2:
            count = get_possibility_count(row, trie)
            print(f"{row}: count: {count}")
            counter += count
print(f"Total Count: {counter}")
