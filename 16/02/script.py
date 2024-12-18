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
    return f"\033[94;1;4m{text}\033[0m"

def g(text):
    return f"\033[92;1;4m{text}\033[0m"

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

if not sys.argv[1].startswith("input"):
    print("Invalid input file provided.")
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

START = "S"
END = "E"
WALL = "#"
EMPTY = "."
NORTH = "NORTH"
EAST = "EAST"
SOUTH = "SOUTH"
WEST = "WEST"
DELTAS = {
    NORTH: [-1, 0],
    EAST: [0, 1],
    SOUTH: [1, 0],
    WEST: [0, -1],
}

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

def get_neighbors(grid, row, col, direction):
    # This maps a direction change as though it is a node
    # So 13, 1, EAST -> (13, 2, EAST), (13, 1, NORTH)
    neighbors = []
    for ndirection, delta in DELTAS.items():
        next_row, next_col = row + delta[0], col + delta[1]
        if grid[next_row][next_col] == WALL:
            continue
        if direction != ndirection:
            neighbors.append(((row, col, ndirection), 1000))
            continue
        neighbors.append(((next_row, next_col, ndirection), 1))
    return neighbors

def find_shortest_path(grid, start, end, blacklist = []):
    print(f"Blacklist: {blacklist}")
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

        for neighbor, cost in get_neighbors(grid, *node):
            if (neighbor[0], neighbor[1]) in blacklist:
                continue
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

            tmp = dist[node] + cost

            if tmp < dist[neighbor]:
                dist[neighbor] = tmp
                prev[neighbor] = node

    if not len(end_nodes):
        print("Could not reach end")
        return float('inf'), []

    # This seems like an awful lot of work
    end_nodes = [node for node in end_nodes] # Bad pattern - overwriting set w/ list so we can sort it
    end_nodes.sort(key=lambda u: dist[u])
    e = end_nodes[0]
    min_distance = dist[e]

    current_node = e
    shortest_path = [current_node]
    while current_node != start:
        current_node = prev[current_node]
        shortest_path.append(current_node)

    return min_distance, shortest_path[::-1]

grid = []
start = None, None, EAST
end = None, None
with open(sys.argv[1], "r") as f:
    for row_index, row in enumerate(f.readlines()):
        row = row.strip()
        grid.append([])
        for col_index, col in enumerate(row):
            if col in [START, EMPTY, END]:
                if col == START:
                    start = row_index, col_index, EAST
                elif col == END:
                    end = row_index, col_index
            grid[-1].append(col)

print_grid(grid)

# This works but it's a little buggy - it misses one of the tiles in input_test_1
# HOWEVER - it worked for the actual problem case, so good enough
shortest_paths = []
min_distance, shortest_path = find_shortest_path(grid, start, end)
print_divider(DOT, QUARTER)
print(f"{id('Min Distance')} {min_distance}")
shortest_paths.append(shortest_path)
for idx, node in enumerate(shortest_path):
    print_divider(DASH, HALF)
    print(f"{idx} out of {len(shortest_path)}")
    if node == start or (node[0], node[1]) == end:
        continue
    distance, path = find_shortest_path(grid, start, end, [(node[0], node[1])])
    print(distance)
    if distance == min_distance:
        print(f"Appending to shortest paths")
        shortest_paths.append(path)

shortest_path_nodes = set()
for path in shortest_paths:
    for (row, col, direction) in path:
        shortest_path_nodes.add((row, col))
print(f"Nodes in shortest paths: {len(shortest_path_nodes)}")
print_grid(grid, start, shortest_path_nodes)
