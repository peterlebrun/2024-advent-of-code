grid = []
success_coords = set()
output_grid = []
count = 0

with open('input', 'r') as f:
    for line in f.readlines():
        grid.append([x for x in line.strip()])

# Find X in strings
# check r, dr, d, dl, l, ul, u, ur

def count_xmas(row, col, grid):
    total = 0
    for delta in [
        ([0,   1], [0,   2], [0,   3]), # E
        ([1,   1], [2,   2], [3,   3]), # SE
        ([1,   0], [2,   0], [3,   0]), # S
        ([1,  -1], [2,  -2], [3,  -3]), # SW
        ([0,  -1], [0,  -2], [0,  -3]), # W
        ([-1, -1], [-2, -2], [-3, -3]), # NW
        ([-1,  0], [-2,  0], [-3,  0]), # N
        ([-1,  1], [-2,  2], [-3,  3]), # NE
    ]:
        M, A, S = delta

        try:
            if ((row + M[0] < 0) or
                (col + M[1] < 0) or
                (row + A[0] < 0) or
                (col + A[1] < 0) or
                (row + S[0] < 0) or
                (col + S[1] < 0)):
                continue

            if (grid[row + M[0]][col+M[1]] == "M" and
                grid[row + A[0]][col+A[1]] == "A" and
                grid[row + S[0]][col+S[1]] == "S"):

                success_coords.add((row, col))
                success_coords.add((row + M[0], col+M[1]))
                success_coords.add((row + A[0], col+A[1]))
                success_coords.add((row + S[0], col+S[1]))

                total += 1

        except IndexError:
            pass

    return total

for row in range(len(grid)):
    row_tmp = f""
    for col in range(len(grid[row])):
        tmp = 0
        if grid[row][col] == "X":
            tmp = count_xmas(row, col, grid)
            count += tmp
        row_tmp = row_tmp + f" {tmp}"
    #print(row_tmp)

print("="*80)
print("\n")
for row in range(len(grid)):
    tmp = f""
    for col in range(len(grid[row])):
        char = grid[row][col]
        if (row, col) in success_coords:
            tmp = tmp + f"\033[96m{char}\033[0m"
        else:
            tmp = tmp + "."
    print(tmp)

print(count)
