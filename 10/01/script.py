import sys
import copy
from collections import defaultdict
import math
sys.setrecursionlimit(1073741824)

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

def print_str(*args):
    print(" ".join(map(str, args)))

def print_divider(divider=EQUAL, length=FULL):
    print(divider*length, "\n")

def exit():
    print_str("Exiting...")
    sys.exit()

if len(sys.argv) < 2:
    print_str("Please specify input file.")
    exit()

if sys.argv[1] not in ["input", "input_test"]:
    print_str("Invalid input file provided. Should be one of ", b("input "),
              "or ", b("input_test"))
    exit()

if len(sys.argv) > 2:
    print_str("Unrecognized arguments provided.")
    exit()

def get_inputs():
    with open(sys.argv[1], "r") as f:
        return [list(map(int, [*f.strip()])) for f in f.readlines()]

grid = get_inputs()

def get_children(graph, accumulator = []):
    #if not graph:
        #return accumulator
    children = []
    for k, v in graph.items():
        new_path = accumulator + [k]
        if v:
            children.extend(get_children(v, new_path))
        else:
            children.append(new_path)
    return children

scores = defaultdict(set)

def eval_neighbors(parent_row, parent_col, parent_val, og):
    #print_str("Evaluating parent", (parent_row, parent_col), parent_val)
    #accum = {}
    for r, c in [
        ( 0,  1),
        ( 1,  0),
        ( 0, -1),
        (-1,  0),
    ]:
        row = parent_row + r
        col = parent_col + c
        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
            #print_str((row, col), "not in grid")
            continue
        val = grid[row][col]
        #print_str("Evaluating child", (row, col), val)
        if val == parent_val + 1:
            if val == 9:
                #print_str("Val is 9")
                #accum[(row, col)] = 9
                scores[og].add((row, col))
            else:
                #print_str("Looking at neighbors")
                eval_neighbors(row, col, val, og)
    #return accum

print_divider()
for row in grid:
    print(row)

def print_children(node, depth = 0):
    depth += 1
    for k, v in node.items():
        if v == 9:
            print(" "*depth, v)
            continue

        print(" "*depth, k)
        print_children(node[k], depth)

print_divider(DASH, HALF)
tree = {}
for row in range(len(grid)):
    for col in range(len(grid[0])):
        if grid[row][col] == 0:
            tree[(row, col)] = eval_neighbors(row, col, 0, (row, col))

#for x in scores:
    #print(x, ":", scores[x])

print(sum([len(v) for k, v in scores.items()]))
