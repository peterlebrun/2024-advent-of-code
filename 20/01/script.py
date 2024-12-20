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

def get_grid_neighbors(grid, row, col):
    neighbors = []
    for delta in [[1,0],[0,1],[-1,0],[0,-1]]:
        next_row, next_col = row + delta[0], col + delta[1]
        if next_row not in range(R) or next_col not in range(C):
            continue
        if grid[next_row][next_col] == WALL:
            continue
        neighbors.append((next_row, next_col))
    return neighbors

def get_node_between(a, b):
    return ((a[0] + b[0])//2, (a[1]+b[1])//2)

def get_path_distance(path_prev, pre, post):
    """
    path_prev maps from node n to node n-1.
    Count number of jumps from post to pre.
    """
    counter = 0
    node = post
    while node != pre:
        node = path_prev[node]
        counter += 1
    return counter

def get_jumps(path, row, col, jump_size):
    jumps = []
    for delta in [
        [jump_size,0],
        [0,jump_size],
        [-1 * jump_size,0],
        [0,-1 * jump_size],
    ]:
        coords = (row + delta[0], col + delta[1])
        if coords in path:
            btw = get_node_between((row, col), coords)
            if grid[btw[0]][btw[1]] == WALL:
                jumps.append([(row, col), coords])
    return jumps

WALL = "#"
EMPTY = "."
START = "S"
END = "E"
grid = []

start_coords = None, None
end_coords = None, None
with open(sys.argv[1], "r") as f:
    for row_index, row in enumerate(f.readlines()):
        row = row.strip()
        grid.append([])
        for col_index, col in enumerate(row):
            if col == START:
                start_coords = row_index, col_index
            if col == END:
                end_coords = row_index, col_index
            grid[-1].append(col)

R = len(grid)
C = len(grid[0])

def find_shortest_path(grid, start=start_coords, end=end_coords):
    dist = {}
    prev = {}
    unvisited_nodes = [start]
    visited_nodes = set()
    dist[start] = 0
    end_nodes = set()
    while len(unvisited_nodes):
        unvisited_nodes.sort(key=lambda u: dist[u])
        node = unvisited_nodes.pop(0)
        visited_nodes.add(node)

        for neighbor in get_grid_neighbors(grid, *node):
            if neighbor in visited_nodes:
                continue
            if (neighbor[0], neighbor[1]) == end:
                end_nodes.add(neighbor)
            elif neighbor not in unvisited_nodes:
                unvisited_nodes.append(neighbor)
            if neighbor not in dist:
                dist[neighbor] = float('inf')
            if neighbor not in prev:
                prev[neighbor] = None

            tmp = dist[node] + 1

            if tmp < dist[neighbor]:
                dist[neighbor] = tmp
                prev[neighbor] = node

    if not len(end_nodes):
        print("Could not reach end")
        return float('inf'), []

    min_distance = dist[end_coords]

    current_node = end_coords
    shortest_path = [end_coords]
    while current_node != start:
        current_node = prev[current_node]
        shortest_path.append(current_node)

    return min_distance, shortest_path[::-1], prev

distance, path, prev = find_shortest_path(grid)

print_divider(DASH, HALF)
print(f"Distance: {distance}")

jumps_to_eval = set()
for node in path:
    print(f"Calculate jumps for {node}")
    for jump in get_jumps(path, node[0], node[1], 2):
        # Ensure always arranged from earlier node to later
        jump.sort(key=path.index)

        if tuple(jump) in jumps_to_eval:
            continue

        jumps_to_eval.add(tuple(jump))

jump_sizes = defaultdict(int)
for pre, post in jumps_to_eval:
    dist = get_path_distance(prev, pre, post) - 2 # Subtract two for initial jump cost
    print(f"Jump from {pre} to {post} saves {dist}")
    jump_sizes[dist] += 1

ge_100 = 0
tmp = list(jump_sizes.keys())
tmp.sort()
for key in tmp:
    if key >= 100:
        ge_100 += jump_sizes[key]
    print(f"{key}: {jump_sizes[key]}")

print_divider(DOT, QUARTER)
print(f"Num ge100: {ge_100}")
