grid = []
success_coords = set()
output_grid = []
count = 0
M = "M"
A = "A"
S = "S"

with open('input', 'r') as f:
    for line in f.readlines():
        grid.append([x for x in line.strip()])

def is_xmas(row, col, grid):
    neighbors = {
        M: [],
        S: [],
    }

    for delta in [
        [ 1,  1],
        [ 1, -1],
        [-1,  1],
        [-1, -1]
    ]:
        try:
            coords = [row + delta[0], col + delta[1]]

            if any([c < 0 for c in coords]):
                continue

            char = grid[coords[0]][coords[1]]

            if char in neighbors:
                neighbors[char].append(coords)

        except IndexError:
            pass

    Ms = neighbors[M]
    Ss = neighbors[S]

    ## We should have two Ms and two Ss. Both Ms should have either the same row
    ## or the same column.
    if (len(Ms) == 2 and
        len(Ss) == 2 and
        (Ms[0][0] == Ms[1][0] or Ms[0][1] == Ms[1][1])):
         return 1

    return 0

for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row][col] == A:
            count += is_xmas(row, col, grid)

print(count)
