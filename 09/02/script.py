import sys
import copy
from collections import defaultdict
import math
sys.setrecursionlimit(1073741824)

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

def print_str(*args):
    print(" ".join(map(str, args)))

def print_divider(divider=EQUAL, length=FULL):
    print(divider*length)

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

def get_inputs():
    with open(sys.argv[1], "r") as f:
        return list(map(int, f.readline().strip()))

FILES = "FILES"
FILE_ENDS = "FILE_ENDS"
FILE_SIZES = "FILE_SIZES"
FILE_STARTS = "FILE_STARTS"
SPACE_SIZES = "SPACE_SIZES"
SPACE_STARTS = "SPACE_STARTS"
UNMOVED_FILE_IDS = "UNMOVED_FILE_IDS"
SPACE = "SPACE"
NUM_BLOCKS = "NUM_BLOCKS"

def parse_inputs(inputs):
    file_id = 0
    location_id = 0
    locations = {
        FILES: [],
        FILE_SIZES: {},
        FILE_STARTS: {},
        SPACE_SIZES: {},
        SPACE_STARTS: [],
    }

    for i in range(len(inputs)):
        digit = inputs[i]

        if i % 2 == 0:
            locations[FILES].insert(0, file_id)
            locations[FILE_STARTS][file_id] = location_id
            locations[FILE_SIZES][file_id] = digit
        else:
            if digit:
                locations[SPACE_STARTS].append(location_id)
                locations[SPACE_SIZES][location_id] = digit

        for j in range(digit):
            locations[location_id] = file_id if i % 2 == 0 else SPACE
            location_id += 1

        if i % 2 == 0:
            file_id += 1

    return locations

def get_checksum(locations):
    cum_sum = 0

    for i, v in locations.items():
        if i in [FILES, FILE_SIZES, FILE_STARTS, SPACE_SIZES, SPACE_STARTS]:
            continue
        if locations[i] == SPACE:
            continue

        start = f"{blue(cum_sum)} + "
        cum_sum += i * v
        add_str = green(f"{i} * {v}")
        sum_str = red(f"= {cum_sum}")
        print_str(start, add_str, sum_str)

    print_divider(DASH, HALF)
    return cum_sum

def print_locations(locations):
    for k, v in locations.items():
        print_str(green(k), blue(v))

def compact(locations):
    locations[FILES].sort(reverse=True)

    for f_idx, f in enumerate(locations[FILES]):
        f_size = locations[FILE_SIZES][f]
        f_start = locations[FILE_STARTS][f]

        for s_start_idx, s_start in enumerate(locations[SPACE_STARTS]):
            if s_start > f_start:
                continue

            s_size = locations[SPACE_SIZES][s_start]

            if f_size <= s_size:
                print_divider()
                print(f"{f_idx} Moving file {f} of size {f_size} to location {s_start} of size {s_size}")

                for x in range(f_size):
                    locations[f_start + x] = SPACE
                    locations[s_start + x] = f

                if f_size < s_size:
                    locations[SPACE_STARTS][s_start_idx] = s_start + f_size
                    locations[SPACE_SIZES][s_start + f_size] = s_size - f_size
                else:
                    del locations[SPACE_STARTS][s_start_idx]

                for i, s in enumerate(locations[SPACE_STARTS]):
                    if i + 1 == len(locations[SPACE_STARTS]):
                        locations[SPACE_STARTS].append(f_start)
                        locations[SPACE_SIZES][f_start] = f_size
                        break
                    if f_start < s:
                        locations[SPACE_STARTS].insert(0, f_start)
                        locations[SPACE_SIZES][f_start] = f_size
                        break

                    prev_start = locations[SPACE_STARTS][i]
                    next_start = locations[SPACE_STARTS][i+1]

                    if f_start > prev_start and f_start < next_start:
                        prev_size = locations[SPACE_SIZES][prev_start]
                        next_size = locations[SPACE_SIZES][next_start]

                        new_start = f_start
                        new_size = f_size

                        if prev_start + prev_size == f_start:
                            new_start = prev_start
                            new_size += prev_size

                        if f_start + f_size == next_start:
                            new_start = min(new_start, f_start)
                            new_size += next_size

                        locations[SPACE_SIZES][new_start] = new_size

                        if new_start < f_start:
                            locations[SPACE_STARTS][i] = new_start
                            if new_size == f_size + prev_size + next_size:
                                del locations[SPACE_STARTS][i+1]
                                del locations[SPACE_SIZES][next_start]
                            break

                        if new_start == f_start and new_size == f_size:
                            locations[SPACE_STARTS].insert(i+1, new_start)
                            break

                        if new_start == f_start and new_size >= f_size:
                            locations[SPACE_STARTS][i+1] = new_start
                            del locations[SPACE_SIZES][next_start]
                            break

                del locations[SPACE_SIZES][s_start]
                locations[FILE_STARTS][f] = s_start

                break

locations = parse_inputs(get_inputs())
compact(locations)

print_divider(DASH, HALF)
print_str("Checksum: ", green(get_checksum(locations)))
print_divider(DASH, HALF)
