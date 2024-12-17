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
OPPOSITE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}
def get_inputs():
    inputs = []
    start_coords = None, None
    with open(sys.argv[1], "r") as f:
        for row_index, row in enumerate(f.readlines()):
            if START in row:
                start_coords = row_index, row.index(START)
            inputs.append([c for c in row.strip()])
    return inputs, start_coords

def print_grid(grid, coords, neighbors, missing_vals=[]):
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
    print(bottom)
    for row_index, row in enumerate(grid):
        output = ""
        for col_index, col in enumerate(row):
            if (row_index, col_index) == coords:
                output += f"{g(col)}"
            elif (row_index, col_index) in neighbors:
                output += f"{b(col)}"
            elif col == WALL:
                output += "\033[37;2m#\033[0m"
            elif (row_index, col_index) in missing_vals:
                output += f"\033[91;1;4m{col}\033[0m"
            else:
                output += f"\033[32;1m{col}\033[0m"
        print(f"{lpad(row_index, 3)}: {output}")

# this is currently implemented as DFS, needs to be BFS
def enqueue(
    queue,
    row,
    col,
    parent_coords,
    prev_direction = EAST,
    path_score = 0,
):
    queue.append((
        row,
        col,
        parent_coords,
        prev_direction,
        path_score,
    ))

def traverse(
    grid = [[]],
    row = 0,
    col = 0,
    parent_coords = (0, 0, EAST),
    prev_direction = EAST,
    vertices = {}
):
    visited_nodes = set()
    unvisited_nodes = []
    enqueue(unvisited_nodes, row, col, parent_coords)
    while len(unvisited_nodes):
        #print(f"Len Unvisited Nodes: {len(unvisited_nodes)}")
        node = unvisited_nodes.pop(0)
        row, col, parent_coords, prev_direction, path_score = node
        print(f"Node: {node}")

        if grid[row][col] == END:
            vertices[parent_coords][END] = path_score
            continue

        neighbors = []
        for direction, delta in DELTAS.items():
            next_row, next_col = row + delta[0], col + delta[1]

            # Don't allow direction reversal
            if direction == OPPOSITE[prev_direction]:
                continue

            if grid[next_row][next_col] == WALL:
                continue

            neighbors.append(((next_row, next_col), direction))

        if not len(neighbors):
            continue

        if len(neighbors) == 1:
            ((next_row, next_col), direction) = neighbors[0]
            if direction != prev_direction:
                vertices[parent_coords][(row, col, prev_direction)] = path_score
                vertices[(row, col, prev_direction)][(row, col, direction)] = 1000
                parent_coords = (row, col, direction)
                path_score = 0

            enqueue(
                unvisited_nodes,
                next_row,
                next_col,
                parent_coords,
                direction,
                path_score + 1
            )
        else:
            if (row, col, prev_direction) not in vertices:
                vertices[(row, col, prev_direction)] = {}

            if (row, col, prev_direction) in vertices[parent_coords]:
                vertices[parent_coords][(row, col, prev_direction)] = min(
                    path_score,
                    vertices[parent_coords][(row, col, prev_direction)],
                )
            else:
                vertices[parent_coords][(row, col, prev_direction)] = path_score

            if (row, col) in visited_nodes:
                continue
            visited_nodes.add((row, col))

            for n in neighbors:
                ((next_row, next_col), direction) = n

                if direction != prev_direction:
                    vertices[(row, col, prev_direction)][(row, col, direction)] = 1000

                enqueue(
                    unvisited_nodes,
                    next_row,
                    next_col,
                    (row, col, direction),
                    direction,
                    1
                )

def do_dijkstra_sort_of(vertices, start_coords, missing_vals):
    dist = {}
    prev = {}
    unvisited = []
    for v in vertices:
        dist[v] = float('inf')
        prev[v] = None
        unvisited.append(v)
    dist[start_coords] = 0
    dist[END] = float('inf')
    prev[END] = None

    while len(unvisited):
        unvisited.sort(key=lambda u: dist[u])
        node = unvisited[0]
        unvisited.remove(node)

        for neighbor, weight in vertices[node].items():
            if neighbor not in dist:
                dist[neighbor] = float('inf')
            if neighbor not in prev:
                prev[neighbor] = None
            tmp_weight = dist[node] + weight

            if tmp_weight < dist[neighbor]:
                dist[neighbor] = tmp_weight
                prev[neighbor] = node
    return dist[END]

min_path_weight = 999999999999999999999
def compute_paths(vertices, coords, path_weight, path, paths):
    global min_path_weight
    for next_coords, weight in vertices[coords].items():
        if next_coords in path:
            continue

        tmp_path = path.copy()
        tmp_weight = path_weight + weight
        if tmp_weight > min_path_weight:
            continue
        tmp_path.append(next_coords)

        if next_coords == END:
            print(f"Found: {tmp_weight}",end="")
            if tmp_weight < min_path_weight:
                min_path_weight = tmp_weight
                paths.append((tmp_path, tmp_weight))
                print(f" Found new min!")
            else:
                print(f" Not less than existing min.")

            return
        else:
            compute_paths(vertices, next_coords, tmp_weight, tmp_path, paths)

grid, start_coords = get_inputs()

print_divider()
print_divider(DASH, HALF)
print(f"Starting Coords: {start_coords}")
print_divider(DOT, QUARTER)

vertices = defaultdict(dict)

traverse(
    grid,
    start_coords[0],
    start_coords[1],
    (*start_coords, EAST),
    EAST,
    vertices,
)

print_grid(grid, start_coords, vertices.keys())
print_divider(DOT, HALF)

print_divider(DOT, HALF)

missing_vals = []
print_grid(grid, start_coords, vertices.keys())

for k, v in vertices.items():
    print(f"{k}: {v}")

print(f"Minimum Path Score: {do_dijkstra_sort_of(vertices, (*start_coords, EAST), missing_vals)}")
