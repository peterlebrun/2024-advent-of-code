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

def blue(text):
    return f"\033[94m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
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
COMPACTED = "COMPACTED"
SPACES = "SPACES"
SPACE = "SPACE"

def parse_inputs(inputs):
    file_id = 0
    location_id = 0
    locations = {
        FILES: [],
        SPACES: [],
        FILE_ENDS: {},
        COMPACTED: [],
    }

    for i in range(len(inputs)):
        digit = inputs[i]
        for j in range(digit):
            if i % 2 == 0:
                locations[location_id] = file_id
                locations[FILES].append(location_id)
            if i % 2 == 1:
                locations[location_id] = SPACE
                locations[SPACES].append(location_id)
            location_id += 1
        if i % 2 == 0:
            locations[FILE_ENDS][file_id] = location_id - 1
            file_id += 1

    return locations

def get_checksum(locations):
    cum_sum = 0

    for i in range(len(locations)):
        start = f"{blue(cum_sum)} + "
        if locations[i] == DOT:
            continue

        to_add = i * locations[i]
        cum_sum += to_add
        print_str(start, green(to_add), red("="), red(cum_sum))

    print_divider(DASH, HALF)
    return cum_sum

def print_locations(locations):
    for k,v in locations.items():
        print_str(green(k), blue(v))

def compact(locations):
    locations[FILES].sort()
    locations[SPACES].sort()

    # By definition, location 0 will contain file block
    locations[COMPACTED].append(locations[FILES].pop(0))

    while max(locations[FILES]) > max(locations[SPACES]):
        # move any contiguous file blocks over when appropriate
        if locations[FILES][0] == locations[COMPACTED][-1] + 1:
            locations[COMPACTED].append(locations[FILES].pop(0))
            continue

        space_location = locations[SPACES].pop(0)
        file_start  = locations[FILES][0] # can't pop because we want file end instead
        file_id = locations[file_start]
        file_end = locations[FILES].pop(locations[FILES].index(locations[FILE_ENDS][file_id]))

        print_str("Next space:", space_location)
        print_str("File start:", file_start)
        print_str("File id:", file_id)
        print_str("File_end:", file_end)

        ## Needs to all happen at "once":
        locations[space_location] = file_id
        locations[file_end] = SPACE
        locations[COMPACTED].append(space_location)
        locations[FILE_ENDS][file_id] -= 1

        for i in range(len(locations[SPACES])):
            if i+1 == len(locations[SPACES]):
                locations[SPACES].append(file_end)
                break

            if file_end > locations[SPACES][i] and file_end < locations[SPACES][i+1]:
                locations[SPACES].insert(i+1, file_end)
                break

        print_locations(locations)
        input()

locations = parse_inputs(get_inputs())
print_locations(locations)

compact(locations)
print_str(compacted_files)
print_str(locations[FILES])
print_str(locations[FILE_ENDS])

#print_divider(DASH, HALF)
#print_str("Checksum: ", green(get_checksum(locations)))
#print_divider(DASH, HALF)
