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

dir_keypad = {
    (0,1): UP,
    (0,2): A,
    (1,0): LEFT,
    (1,1): DOWN,
    (1,2): RIGHT,
}

dirs_to_coords = {
    UP: (0,1),
    A: (0,2),
    LEFT: (1,0),
    DOWN: (1,1),
    RIGHT: (1,2),
}

num_keypad = {
    (0,0): "7",
    (0,1): "8",
    (0,2): "9",
    (1,0): "4",
    (1,1): "5",
    (1,2): "6",
    (2,0): "1",
    (2,1): "2",
    (2,2): "3",
    (3,1): "0",
    (3,2): "A",
}

num_to_coords = {
     7: (0,0),
     8: (0,1),
     9: (0,2),
     4: (1,0),
     5: (1,1),
     6: (1,2),
     1: (2,0),
     2: (2,1),
     3: (2,2),
     0: (3,1),
     A: (3,2),
}

dirpad = """
 ^A
<v>
"""

dir_mapping = {
    A:     {                       DOWN: RIGHT, LEFT: UP,   A:A },
    UP:    {         RIGHT: A,     DOWN: DOWN,             A: UP,},
    DOWN:  {RIGHT: RIGHT, UP: UP,              LEFT: LEFT, A: DOWN, },
    LEFT:  {         RIGHT: DOWN,                          A: LEFT,  },
    RIGHT: { UP: A,                             LEFT: DOWN, A: RIGHT, },
}

costs_from_A = {
    A: 0,
    UP: 1,
    RIGHT: 1,
    DOWN: 2,
    LEFT: 3,
}

numpad = """
789
456
123
 0A
"""

num_mapping = {
     '7': { RIGHT: '8',          DOWN: '4',          A: '7' },
     '8': { RIGHT: '9',          DOWN: '5', LEFT: '7', A: '8', },
     '9': {                      DOWN: '6', LEFT: '8', A: '9' },
     '4': { RIGHT: '5', UP: '7', DOWN: '1',           A: '4',},
     '5': { RIGHT: '6', UP: '8', DOWN: '2', LEFT: '4', A: '5' },
     '6': {             UP: '9', DOWN: '3', LEFT: '5', A: '6' },
     '1': { RIGHT: '2', UP: '4',                      A: '1' },
     '2': { RIGHT: '3', UP: '5', DOWN: '0', LEFT: '1', A: '2' },
     '3': {             UP: '6', DOWN: 'A', LEFT: '2', A: '3' },
     '0': { RIGHT: 'A', UP: '2',                     A: '0' },
      A : {             UP: '3', LEFT: '0'           ,A: A },
}

START = A
def get_paths(start, neighbors=dir_mapping, weights=None):
    paths = {
        n: {
            "dist": 0 if n == start else float('inf'),
            "path": [],
        }
        for n in neighbors
    }

    unvisited_nodes = [start]
    visited_nodes = set()
    while len(unvisited_nodes):
        unvisited_nodes.sort(key=lambda u: paths[u]["dist"])
        node = unvisited_nodes.pop(0)
        visited_nodes.add(node)

        for direction, neighbor in neighbors[node].items():
            if neighbor in visited_nodes:
                continue
            if neighbor not in unvisited_nodes:
                unvisited_nodes.append(neighbor)

            tmp = paths[node]["dist"] + (1 if not weights else weights[direction])
            if tmp < paths[neighbor]["dist"]:
                paths[neighbor]["dist"] = tmp
                paths[neighbor]["path"] = paths[node]["path"] + [direction]

    return paths

def get_num_paths(start, neighbors=num_mapping):
    paths = {
        n: {
            "dist": 0 if n == start else float('inf'),
            "path": [],
        }
        for n in neighbors
    }

    unvisited_nodes = [start]
    visited_nodes = set()
    while len(unvisited_nodes):
        unvisited_nodes.sort(key=lambda u: paths[u]["dist"])
        node = unvisited_nodes.pop(0)
        visited_nodes.add(node)

        for direction, neighbor in neighbors[node].items():
            if neighbor in visited_nodes:
                continue
            if neighbor not in unvisited_nodes:
                unvisited_nodes.append(neighbor)

            tmp = paths[node]["dist"] + 1

            if tmp < paths[neighbor]["dist"]:
                paths[neighbor]["dist"] = tmp
                paths[neighbor]["path"] = paths[node]["path"] + [direction]

    return paths

def populate_shortest_paths(mapping=dir_mapping, get_weight=None):
    output = {}
    for start in mapping:
        for end, path in get_paths(start, mapping, get_weight).items():
            output[(start, end)] = path["path"] + [A]
    return output

dir_paths = populate_shortest_paths()
for x in dir_paths:
    print(x, dir_paths[x])

num_paths = populate_shortest_paths(num_mapping, costs_from_A)

def get_path(path, mapping=dir_paths):
    output = ""
    prev = START # First move is always coming from A
    for i in range(len(path)):
        output += "".join(mapping[(prev, path[i])])
        prev = path[i]
    return output

#for p in [">^>", "^>>", ">>^"]:
    #print(p, get_path(p), len(get_path(p)))

with open(sys.argv[1], "r") as f:
    inputs = [[c for c in row.strip()] for row in f.readlines()]

for row in inputs:
    print_divider()
    prev = START
    print("".join(row))
    r1=get_path(row, num_paths)
    print(r1)
    r2=get_path(r1)
    print(r2)
    me=get_path(r2)
    print(me, len(me))

sys.exit()

def print_nicely(row, num_path, accum):
    row_output = ""
    num_path_output = ""
    d0_output = ""
    d1_output = ""

    d0_counter = 0
    d1_counter = 0

    if len(num_path) > 4:
        print("ruh roh, fucking error")
        return

    while len(num_path):
        row_step = row.pop(0)
        step = num_path.pop(0)

        for step_i in step:
            d0_steps = []
            d1_steps = []
            d0_steps.extend(accum[0].pop(0))

            for i in d0_steps:
                for _ in range(len(i)):
                    d1_steps.append(accum[1].pop(0))

            tmp0 = ""
            tmp1 = ""
            while len(d1_steps):
                d1 = "".join(d1_steps.pop(0))
                d0 = lpad(d0_steps.pop(0), len(d1))
                tmp1 += d1
                tmp0 += d0
            num_path_output += lpad(step_i, len(tmp1)) + "|"
            d0_output += tmp0 + "|"
            d1_output += tmp1 + "|"

    print_divider(DASH, len(d1_output))
    print(num_path_output)
    print("         <|         A|       ^|   A|       >|  ^|^|   A|        v|v|v|      A|")
    print(d0_output)
    print("  v <<   A| >  >  ^ A|   <   A| > A|   v   A|<^A|A| > A|  < v   A|A|A| >  ^ A|")
    print(d1_output)
    print(
"<vA<AA>>^A|vAA<^A>A  |<v<A>>^A|vA^A|<vA>^A|<v<A|>^A>AA|vA^A|<v<A>A>^A|A|A|vA<^A>A|"
        )

#v1 = "<A^A>^^AvvvA"
#v2 = "<A^A^>^AvvvA"
#v3 = "<A^A^^>AvvvA"
#
#print(v1)
#print(v2)
#print(v3)
#print_divider()
#print("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")
#print(get_path(v1))
#print(get_path(v2))
#print(get_path(v3))
#print_divider()
#print("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
#print(get_path(get_path(v1)))
#print(get_path(get_path(v2)))
#print(get_path(get_path(v3)))
#print(len(get_path(get_path(v3))))
#
#print_divider()
#print(get_path("v<<A>>^A<A>AvA<^AA>A<vAAA>^A"))
#print(len(get_path("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")))
#
#print_divider()
#print(get_path("v<<A>>^A<A>AvA^<AA>Av<AAA^>A"))
#print(len(get_path("v<<A>>^A<A>AvA^<AA>Av<AAA^>A")))

    # split num_path on A
    # get char count for diff parts
    # if char count >1: get permutations
    # create longer paths for each permutation; get shortest one

    #print(len(num_path))
    #for i in row:
    #print(f"Num Path: {num_path}")
    #print(f"{k}: Len: {len(accum[k])}   {accum[k]}")
    #print_nicely(row, num_path, accum)
    #break

#for key, path in num_paths.items():
#    print(f"{key}, {path}")

#<<vAA>A>^AAvA<^A>AvA^A<<vA>>^AAvA^A<vA>^AA<A>A<<vA>A>^AAAvA<^A>A
#<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

numpad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],
]

dirpad = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]

#def simulate(instructions):
    #numpad_start = (3, 2)
    #r2_start = (0, 2)
    #r1_start = (0, 2)

#print_grid(numpad)
#print_grid(dirpad)

def u(text):
    return f"\033[4m{text}\033[0m"

def print_state(human_state, r1_state, r2_state, numpad_state, path):
    header = f"\t{u('human')}\t {u('r1')}\t {u('r2')}\t{u('numpad')}"
    output = [
        "\t"*4 + "   ",
        "\t  ",
        "\t  ",
        "\t"*4 + "   ",
    ]

    for row_index, row in enumerate(dirpad):
        for col_index, col in enumerate(row):
            if (row_index, col_index) in []:
                output[row_index+1] += f"{g(col)}"
            elif (row_index, col_index) in path:
                output[row_index+1] += f"\033[94;1m{col}\033[0m"
            else:
                output[row_index+1] += f"\033[32m{col}\033[0m"
        output[row_index+1] += "\t"

    for row_index, row in enumerate(dirpad):
        for col_index, col in enumerate(row):
            if (row_index, col_index) in []:
                output[row_index+1] += f"{g(col)}"
            elif (row_index, col_index) in path:
                output[row_index+1] += f"\033[94;1m{col}\033[0m"
            else:
                output[row_index+1] += f"\033[32m{col}\033[0m"
        output[row_index+1] += "\t"

    for row_index, row in enumerate(dirpad):
        for col_index, col in enumerate(row):
            if (row_index, col_index) in []:
                output[row_index+1] += f"{g(col)}"
            elif (row_index, col_index) in path:
                output[row_index+1] += f"\033[94;1m{col}\033[0m"
            else:
                output[row_index+1] += f"\033[32m{col}\033[0m"
        output[row_index+1] += "\t   "

    for row_index, row in enumerate(numpad):
        for col_index, col in enumerate(row):
            if (row_index, col_index) in []:
                output[row_index] += f"{g(col)}"
            elif (row_index, col_index) in path:
                output[row_index] += f"\033[94;1m{col}\033[0m"
            else:
                output[row_index] += f"\033[32m{col}\033[0m"

    print(header)
    for row in output:
        print(row)

deltas = {
    UP:    (-1,  0),
    DOWN:  ( 1,  0),
    LEFT:  ( 0, -1),
    RIGHT: ( 0,  1),
}

def add(a,b):
    return a[0] + b[0], a[1] + b[1]

def simulate(instructions):
    state = [((0, 2), (0, 2), (3, 2))]
    output = []

    for i in instructions:
        r1, r2, numpad = state[-1]

        next_r1 = r1
        next_r2 = r2
        next_numpad = numpad
        tmp_output = [i]
        if i == A:
            if r1 not in dir_keypad:
                print(f"Illegal instruction encountered at r1! {r1} not in dir_keypad")
                return

            r1_i = dir_keypad[r1]
            tmp_output.append(r1_i)
            if r1_i == A:
                if r2 not in dir_keypad:
                    print(f"Illegal instruction encountered at r2! {r2} not in dir_keypad")
                    return
                r2_1 = dir_keypad[r2]
                tmp_output.append(r2_1)
                if r2_1 == A:
                    if numpad not in num_keypad:
                        print(f"Illegal instruction encountered at numpad! {numpad} not in dir_keypad")
                        return
                    print(f"Pressing: {num_keypad[numpad]}")
                else:
                    next_numpad = add(numpad, deltas[r2_1])
            else:
                tmp_output.append(" ")
                # update r2 state
                next_r2 = add(r2, deltas[r1_i])
        else:
            next_r1 = add(r1, deltas[i])
            tmp_output.extend([" ", " ", " "])

        next_state = (next_r1, next_r2, next_numpad)
        state.append(next_state)
        output.append(tmp_output)

    #print("".join([dir_keypad[s[0]] for s in state])) # r1
    #print("".join([dir_keypad[s[1]] for s in state])) # r2
    #print("".join([num_keypad[s[2]] for s in state])) # numpad
    print_divider(DASH, HALF)
    print("".join([o[0] for o in output])) # r1
    print("".join([o[1] for o in output])) # r2
    print("".join([o[2] for o in output])) # numpad

simulate("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
"""
<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
  v <<   A   > >^  A<A>AvA<^AA>A<vAAA>^A
         <         A^A>^^AvvvA
"""

complexity = 0
for row in inputs:
    print_divider(DOT, HALF)
    print(f"Row: {''.join(row)}")
    row_num = int("".join(row[0:3]))
    num_path = get_path(row, num_paths)
    int_path = get_path(num_path)
    path = get_path(int_path)
    print(num_path)
    #print("<A^A>^^AvvvA")
    print(int_path)
    #print("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")
    print(path)
    #print("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
    print(f"Path Len: {len(path)}")
    complexity += row_num * len(path)
    print(f"Complexity: {row_num * len(path)}")
    simulate(path)
    input()
print(f"Complexity: {complexity}")


"""
"<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
"v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A>^AA<A>Av<A<A>>^AAAvA^<A>A"
"""
