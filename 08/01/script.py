import sys
import copy
from collections import defaultdict
import math
sys.setrecursionlimit(1073741824)

def blue(text):
    return f"\033[94m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

def print_str(*args):
    print(" ".join(args))

def print_divider(divider="=", length=80):
    print(divider*length, "\n")

def exit():
    print_str("Exiting...")
    sys.exit()

if len(sys.argv) < 2:
    print_str("Please specify input file.")
    exit()
if sys.argv[1] not in ["input", "input_test"]:
    print_str("Invalid input file provided. Should be one of ", blue("input "),
              "or ", blue("input_test"))
    exit()
if len(sys.argv) > 2:
    print_str("Unrecognized arguments provided.")
    exit()

INPUT = sys.argv[1]

DOT = "."
STAR = "*"
HASH = "#"

with open(INPUT, "r") as f:
    inputs = [[c for c in r.strip()] for r in f.readlines()]

num_rows = len(inputs)
num_cols = len(inputs[0])

for row in range(num_rows):
    for col in range(num_cols):
        pass
        char = inputs[row][col]
antennas = defaultdict(list)
        if char != DOT:
            antennas[char].append((row, col))

def add(point, vec):
    return (point[0] + vec[0], point[1] + vec[1])

def negate(vec):
    return (-vec[0], -vec[1])

def get_distance_from_origin(point):
    (y, x) = point
    return math.sqrt(x**2 + y**2)

def get_diff_vector(closer, farther):
    if closer == farther:
        return (0, 0)

    return (farther[0] - closer[0], farther[1] - closer[1])

def orient_points(a, b):
    if a == b:
        return a, b

    dist_a = get_distance_from_origin(a)
    dist_b = get_distance_from_origin(b)

    if dist_a < dist_b:
        return a, b
    elif dist_a > dist_b:
        return b, a
    else: # same distance from origin, use the one that's closer to the top
        if a[0] < b[0]:
            return a, b
        else:
            return b, a

def is_valid(point):
    row, col = point

    return not (row < 0 or col < 0 or row >= num_rows or col >= num_cols)

handled_pairs = set()
antinodes = set()
current_char = None
for antenna, all_coords in antennas.items():
    counter = 0
    local_antinodes = set()
    print_divider()
    print(f"{antenna}: {len(all_coords)}")
    print("-" * 10)
    for first in all_coords:
        for second in all_coords:
            counter += 1
            eval_str = f"{counter} {first}, {second}\t"
            if first == second:
                counter -= 1
                continue

            closer, farther = orient_points(first, second)

            if (closer, farther) in handled_pairs:
                print_str(eval_str, blue("Already handled"))
                continue

            diff_vec = get_diff_vector(closer, farther)

            tmp_antinodes = [
                add(closer, negate(diff_vec)),
                add(farther, diff_vec),
            ]

            antinode_strs = []
            for a in tmp_antinodes:
                if is_valid(a):
                    local_antinodes.add(a)
                    antinodes.add(a)
                    antinode_strs.append(green(a))
                else:
                    antinode_strs.append(red(a))

            handled_pairs.add((closer, farther))

            print_str(eval_str, *antinode_strs)

    print("-" * 20)
    print(f"Local antinodes: {len(local_antinodes)}")
    print("-" * 20)
    for r in range(len(inputs)):
        output_str = ""
        for c in range(len(inputs[r])):
            if (r, c) in all_coords:
                output_str += green(inputs[r][c])
            elif (r, c) in local_antinodes:
                output_str += blue(HASH)
            else:
                output_str += inputs[r][c]
        print(output_str)

print_divider("-", 30)
print(f"Total antinodes: {len(antinodes)}")
