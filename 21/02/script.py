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
WALL = "#"

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

def print_grid(grid, coords=set(), neighbors=set(), print_headers = True, missing_vals=[]):
    if print_headers:
        top = " " * 4
        middle = " " * 4
        bottom = ""
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
        print(f"{' ' * 4}\033[4m{bottom}\033[0m")
    for row_index, row in enumerate(grid):
        output = ""
        for col_index, col in enumerate(row):
            if (row_index, col_index) in coords:
                output += f"{g(col)}"
            elif (row_index, col_index) in neighbors:
                output += f"\033[94;1m{col}\033[0m"
            elif col == WALL:
                output += "\033[37;2m#\033[0m"
            elif (row_index, col_index) in missing_vals:
                output += f"\033[91;1;4m{col}\033[0m"
            else:
                output += f"\033[32m{col}\033[0m"
        print(f"{lpad(row_index, 2)}: {output}")

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
LEFT = "<"
DOWN = "v"
RIGHT = ">"
A = "A"

dir_mapping = {
    A:     {                       DOWN: RIGHT, LEFT: UP   },
    UP:    { RIGHT: A,             DOWN: DOWN,             },
    DOWN:  { RIGHT: RIGHT, UP: UP,              LEFT: LEFT },
    LEFT:  { RIGHT: DOWN,                                  },
    RIGHT: {               UP: A,               LEFT: DOWN },
}

num_mapping = {
     '7': { RIGHT: '8',                     DOWN: '4', },
     '8': { RIGHT: '9',          LEFT: '7', DOWN: '5', },
     '9': {                      LEFT: '8', DOWN: '6', },
     '4': { RIGHT: '5', UP: '7',            DOWN: '1', },
     '5': { RIGHT: '6', UP: '8', LEFT: '4', DOWN: '2', },
     '6': {             UP: '9', LEFT: '5', DOWN: '3', },
     '1': { RIGHT: '2', UP: '4',                       },
     '2': { RIGHT: '3', UP: '5', LEFT: '1', DOWN: '0', },
     '3': {             UP: '6', LEFT: '2', DOWN: 'A', },
     '0': { RIGHT: 'A', UP: '2',                       },
      A : {             UP: '3', LEFT: '0',            },
}

dir_paths = {
    ('A', 'A'): ['A'],
    ('A', '^'): ['<', 'A'],
    ('A', 'v'): ['v', '<', 'A'],
    ('A', '<'): ['v', '<', '<', 'A'],
    ('A', '>'): ['v', 'A'],
    ('^', 'A'): ['>', 'A'],
    ('^', '^'): ['A'],
    ('^', 'v'): ['v', 'A'],
    ('^', '<'): ['v', '<', 'A'],
    ('^', '>'): ['>', 'v', 'A'],
    ('v', 'A'): ['>', '^', 'A'],
    ('v', '^'): ['^', 'A'],
    ('v', 'v'): ['A'],
    ('v', '<'): ['<', 'A'],
    ('v', '>'): ['>', 'A'],
    ('<', 'A'): ['>', '>', '^', 'A'],
    ('<', '^'): ['>', '^', 'A'],
    ('<', 'v'): ['>', 'A'],
    ('<', '<'): ['A'],
    ('<', '>'): ['>', '>', 'A'],
    ('>', 'A'): ['^', 'A'],
    ('>', '^'): ['^', '<', 'A'],
    ('>', 'v'): ['<', 'A'],
    ('>', '<'): ['<', '<', 'A'],
    ('>', '>'): ['A'],
}

def get_path(path, mapping=dir_paths):
    output = []
    prev = A
    for i in range(len(path)):
        output += mapping[(prev, path[i])]
        prev = path[i]
    return output

def get_path_str(path, mapping=dir_paths):
    output = ""
    prev = A
    for i in range(len(path)):
        output += "".join(mapping[(prev, path[i])])
        prev = path[i]
    return output

def get_paths(start, neighbors=num_mapping):
    paths = defaultdict(dict)
    visited_nodes = set()

    unvisited_nodes = [(start, A)]
    paths[(start, A)] = {
        "dist": 0,
        "path": [],
    }
    while len(unvisited_nodes):
        unvisited_nodes.sort(key=lambda u: paths[u]["dist"])
        node = unvisited_nodes.pop(0)
        visited_nodes.add(node)

        for direction, neighbor in neighbors[node[0]].items():
            if (neighbor, direction) in visited_nodes:
                continue
            if (neighbor, direction) not in unvisited_nodes:
                unvisited_nodes.append((neighbor, direction))
            if (neighbor, direction) not in paths:
                paths[(neighbor, direction)] = {
                    "dist": float("inf"),
                    "path": [],
                }

            tmp_path = paths[node]["path"]
            prev_move = A if not len(tmp_path) else tmp_path[-1]
            next_path = get_path(dir_paths[(prev_move, direction)])
            weight = len(next_path)

            tmp = paths[node]["dist"] + weight

            if tmp < paths[(neighbor, direction)]["dist"]:
                paths[(neighbor, direction)]["dist"] = tmp
                paths[(neighbor, direction)]["path"] = paths[node]["path"] + [direction]

    for _, path in paths.items():
        prev_move = A if not len(path["path"]) else path["path"][-1]
        next_path = get_path(dir_paths[(prev_move, A)])
        path["dist"] += len(next_path)

    return paths

def populate_shortest_paths(mapping=num_mapping):
    output = {}
    for start in mapping:
        dists = {}
        for (end, _), path in get_paths(start, mapping).items():
            if end in dists:
                if path["dist"] >= dists[end]:
                    continue
            output[(start, end)] = path["path"] + [A]
            dists[end] = path["dist"]
    return output

num_paths = populate_shortest_paths(num_mapping)

with open(sys.argv[1], "r") as f:
    inputs = [[c for c in row.strip()] for row in f.readlines()]

total = 0
for row in inputs:
    print_divider()
    prev = A
    num = int("".join(row[0:3]))
    prev = get_path_str(row, num_paths)
    print(prev)
    for i in range(24):
        prev = get_path_str(prev)
        print(f"{i}: {len(prev)}")
    length = len(prev)
    complexity = length * num
    #print("".join(row))
    #print(num)
    #print(prev)
    #print(prev, length)
    print(complexity)
    total += complexity
print(f"Total: {total}")
