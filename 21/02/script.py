import sys
import copy
from collections import defaultdict
import math
from functools import cache
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

# honestly this is embarassing and no one should use it
num_paths = {
    ("A", "0"): [LEFT, A],
    ("A", "1"): [UP, LEFT, LEFT, A],
    ("A", "3"): [UP, A],
    ("A", "4"): [UP, UP, LEFT, LEFT, A],
    ("A", "5"): [LEFT, UP, UP, A],
    ("A", "8"): [LEFT, UP, UP, UP, A],
    ("A", "9"): [UP, UP, UP, A],
    ("0", "A"): [RIGHT, A],
    ("0", "2"): [UP, A],
    ("1", "3"): [RIGHT, RIGHT, A],
    ("1", "7"): [UP, UP, A],
    ("3", "A"): [DOWN, A],
    ("2", "9"): [UP, UP, RIGHT, A],
    ("3", "4"): [LEFT, LEFT, UP, A],
    ("3", "7"): [LEFT, LEFT, UP, UP, A],
    ("3", "9"): [UP, UP, A],
    ("4", "0"): [RIGHT, DOWN, DOWN, A],
    ("4", "1"): [DOWN, A],
    ("4", "5"): [RIGHT, A],
    ("5", "6"): [RIGHT, A],
    ("5", "8"): [UP, A],
    ("6", "A"): [DOWN, DOWN, A],
    ("6", "8"): [LEFT, UP, A],
    ("7", "9"): [RIGHT, RIGHT, A],
    ("8", "A"): [DOWN, DOWN, DOWN, RIGHT, A],
    ("8", "0"): [DOWN, DOWN, DOWN, A],
    ("8", "3"): [DOWN, DOWN, RIGHT, A],
    ("8", "6"): [DOWN, RIGHT, A],
    ("9", "A"): [DOWN, DOWN, DOWN, A],
    ("9", "6"): [DOWN, A],
    ("9", "8"): [LEFT, A],
}

dir_paths = {
    ('A', 'A'): ['A'],
    ('A', '^'): ['<', 'A'],
    ('A', 'v'): ['<', 'v', 'A'],
    ('A', '<'): ['v', '<', '<', 'A'],
    ('A', '>'): ['v', 'A'],
    ('^', 'A'): ['>', 'A'],
    ('^', '^'): ['A'],
    ('^', 'v'): ['v', 'A'],
    ('^', '<'): ['v', '<', 'A'],
    ('^', '>'): ['v', '>', 'A'],
    ('v', 'A'): ['^', '>', 'A'],
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
    ('>', '^'): ['<', '^', 'A'],
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

MAX_DEPTH = 24 # # robots - 1 (start at index 0)
@cache
def get_num_steps(pre, post, depth=0):
    path = dir_paths[(pre, post)]

    if depth == MAX_DEPTH:
        return len(path)

    length = 0
    current = A
    for p in path:
        length += get_num_steps(current, p, depth+1)
        current = p
    return length

def get_path_length(path):
    path_length = 0
    prev = A
    for i in range(len(path)):
        next_path = num_paths[(prev, path[i])]
        next_prev = A
        for j in range(len(next_path)):
            path_length += get_num_steps(next_prev, next_path[j])
            next_prev = next_path[j]
        prev = path[i]
    return path_length

with open(sys.argv[1], "r") as f:
    inputs = [[c for c in row.strip()] for row in f.readlines()]

total = 0
new_total = 0
for row in inputs:
    print_divider()
    prev = A
    num = int("".join(row[0:3]))
    r1 = get_path_str(row, num_paths)
    r2 = get_path_str(r1)
    r3 = get_path_str(r2)
    me = get_path_str(r3)
    length = len(me)
    complexity = length * num
    print("".join(row))
    print(num)
    print(r1, len(r1))
    print(r2, len(r2))
    print(me, len(me))
    new_get_path_length = get_path_length(row)
    print("New function:", new_get_path_length)
    new_complexity = new_get_path_length * num
    print("New complexity:", new_complexity)
    print(len(me) * num)
    total += len(me) * num
    new_total += new_complexity
print(f"Total: {total}")
print(f"New Total: {new_total}")

### Below is no longer used

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
        path["path"] += [A]
        path["dist"] += len(next_path)

    return paths

def populate_shortest_paths_old(mapping=num_mapping):
    output = {}
    for start in mapping:
        dists = {}
        for (end, _), path in get_paths(start, mapping).items():
            if end in dists:
                if path["dist"] >= dists[end]:
                    continue
            output[(start, end)] = path["path"]
            dists[end] = path["dist"]
    return output

def get_shortest_path(start, end, neighbors=dir_mapping, depth = 0):
    pad = "-" * depth + (">" if depth else "")

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

            next_path = None
            if depth == MAX_DEPTH:
                next_path = dir_paths[(prev_move, direction)]
            else:
                next_path = get_shortest_path(prev_move, direction, depth=depth + 1)

            tmp = paths[node]["dist"] + len(next_path)

            if tmp < paths[(neighbor, direction)]["dist"]:
                paths[(neighbor, direction)]["dist"] = tmp
                paths[(neighbor, direction)]["path"] = paths[node]["path"] + [direction]

    dists = {}
    for (e, d), path in paths.items():
        prev_move = A if not len(path["path"]) else path["path"][-1]
        next_path = (
            get_path(dir_paths[(prev_move, A)])
            if depth == MAX_DEPTH
            else get_shortest_path(prev_move, A, depth=depth + 1)
        )
        path["path"] += [A]
        path["dist"] += len(next_path)

        if e in dists:
            if path["dist"] >= dists[e]:
                continue

        memos[(start, e, depth)] = path["path"]
        dists[e] = path["dist"]

    return memos[(start, end, depth)]

def populate_shortest_num_paths():
    output = {}
    for start in num_mapping:
        for end in num_mapping:
            output[(start, end)] = get_shortest_path(start, end, num_mapping)
    return output
