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
WALL = "#"
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

R = 71
C = 71
grid = []
for i in range(R):
    grid.append(["."] * C)

def get_neighbors(grid, row, col):
    neighbors = []
    for delta in [[1,0],[0,1],[-1,0],[0,-1]]:
        next_row, next_col = row + delta[0], col + delta[1]
        if next_row not in range(R) or next_col not in range(C):
            continue
        if grid[next_row][next_col] == WALL:
            continue
        neighbors.append((next_row, next_col))
    return neighbors

def find_shortest_path(grid, start, end):
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

        for neighbor in get_neighbors(grid, *node):
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

with open(sys.argv[1], "r") as f:
    walls = [tuple(map(int, r.strip().split(",")[::-1])) for r in f.readlines()]

for index, (row, col) in enumerate(walls):
    if index == 1024:
        break
    grid[row][col] = WALL
print_grid(grid)

START = (0, 0)
END = (R-1, C-1)
distance, path = find_shortest_path(grid, START, END)
print_grid(grid, (), path)
print(f"Distance: {distance}")
