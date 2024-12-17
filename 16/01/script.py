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

def traverse(
    grid = [[]],
    row = 0,
    col = 0,
    parent_coords = (0, 0),
    prev_direction = EAST,
    path_score = 0,
    vertices={},
    nodes=set(),
):
    if (row, col, prev_direction) in nodes:
        return

    if grid[row][col] == END:
        vertices[parent_coords][END] = path_score
        return

    neighbors = []
    for direction, delta in DELTAS.items():
        next_row, next_col = row + delta[0], col + delta[1]

        # Don't allow direction reversal
        if direction == OPPOSITE[prev_direction]:
            continue

        if grid[next_row][next_col] == WALL:
            continue

        neighbors.append(((next_row, next_col), direction))

    if (row, col) == (135, 5):
        print(f"{(row, col)}: {neighbors}")
        input()

    if (row, col) == (119, 3):
        print(f"{(row, col)}: {neighbors}")
        input()

    if not len(neighbors):
        return

    if len(neighbors) == 1:
        ((next_row, next_col), direction) = neighbors[0]

        traverse(
            grid=grid,
            row=next_row,
            col=next_col,
            parent_coords=parent_coords,
            prev_direction=direction,
            path_score=path_score + 1 + (0 if direction == prev_direction else 1000),
            vertices=vertices,
            nodes=nodes,
        )
    else:
        nodes.add((row, col, prev_direction))
        for n in neighbors:
            if (row, col) not in vertices:
                vertices[(row, col)] = {}
            if (row, col) in vertices[parent_coords]:
                vertices[parent_coords][(row, col)] = min(path_score, vertices[parent_coords][(row, col)])
            else:
                vertices[parent_coords][(row, col)] = path_score

            ((next_row, next_col), direction) = n
            traverse(
                grid=grid,
                row=next_row,
                col=next_col,
                parent_coords=(row, col),
                prev_direction=direction,
                path_score=1 + (0 if direction == prev_direction else 1000),
                vertices=vertices,
                nodes=nodes,
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

    while len(unvisited):
        #print(f"Unvisited Before Sort: {unvisited}")
        unvisited.sort(key=lambda u: dist[u])
        node = unvisited[0]
        unvisited.remove(node)

        print(f"Node: {node}")
        print(f"Vertices: {vertices[node]}")
        print(f"Dist Node: {dist[node]}")
        #print(f"Unvisited After Sort: {unvisited}")
        #print(f"Dist Before: {dist}")
        for neighbor, weight in vertices[node].items():
            print(f"neighbor: {neighbor}")
            print(dist[neighbor])
            tmp_weight = dist[node] + weight

            if tmp_weight < dist[neighbor]:
                dist[neighbor] = tmp_weight
                prev[neighbor] = node
            print(f"Dist Neighbor: {dist[neighbor]}")
            print(f"prev neighbor: {prev[neighbor]}")
    print(f"Dist After: {dist}")
    return dist[END], prev

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
nodes = set()
traverse(
    grid=grid,
    row=start_coords[0],
    col=start_coords[1],
    parent_coords=start_coords,
    prev_direction=EAST,
    path_score=0,
    vertices=vertices,
    nodes=nodes,
)

print_grid(grid, start_coords, vertices.keys())
print_divider(DOT, HALF)
for n in nodes:
    print(n)

#for k, v in vertices.items():
    #print(f"{k}: {v}")

print_divider(DOT, HALF)

missing_vals = []
print(f"Minimum Path Score: {do_dijkstra_sort_of(vertices, start_coords, missing_vals)}")

#print_grid(grid, start_coords, vertices.keys(), missing_vals)
