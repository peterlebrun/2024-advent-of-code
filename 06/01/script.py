N = "N"
E = "E"
S = "S"
W = "W"

HASH = "#"

DIRS = {
    N: E,
    E: S,
    S: W,
    W: N
}

VECS = {
    N: (-1,  0),
    E: ( 0,  1),
    S: ( 1,  0),
    W: ( 0, -1),
}

starting_direction = N
starting_coords = (0, 0)
grid = []

def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])

row_counter = 0
with open('input', 'r') as f:
    for row in f.readlines():
        if "^" in row:
            starting_coords = (row_counter, row.find("^"))
        grid.append([c for c in row.strip()])
        row_counter += 1

print(f"start_row: {starting_coords[0]}")
print(f"start_col: {starting_coords[1]}")

direction = starting_direction
coords = starting_coords
should_continue = True
visited_coords = set([coords])

while should_continue:
    next_coords = plus(coords, VECS[direction])
    r, c = next_coords

    if (r < 0 or
        c < 0 or
        r == len(grid) or
        c == len(grid[r])):
        should_continue = False
        break

    if grid[r][c] == HASH:
        direction = DIRS[direction]
        continue

    coords = next_coords
    visited_coords.add(coords)

print(len(visited_coords))
