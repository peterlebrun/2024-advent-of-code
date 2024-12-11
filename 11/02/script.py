import sys
import copy
from collections import defaultdict
import math
import itertools
sys.setrecursionlimit(1073741824)

ZERO = "0"
ONE = "1"
DOT = "."
STAR = "*"
HASH = "#"
DASH = "-"
EQUAL = "="
START = "START"
END = "END"
CYCLE = "CYCLE"
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
    spaces = length - len(text)
    return f"{text}{' ' * spaces if spaces > 0 else ''}"

def id(num):
    return b(rpad(f"{num}:", 12))

def print_divider(divider=EQUAL, length=FULL):
    print(divider*length, "\n")

def exit():
    print("Exiting...")
    sys.exit()

if len(sys.argv) < 2:
    print("Please specify input file.")
    exit()

if sys.argv[1] not in ["input", "input_test"]:
    print("Invalid input file provided. Should be one of ", b("input "),
              "or ", b("input_test"))
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

def get_inputs():
    with open(sys.argv[1], "r") as f:
        return f.readline().strip().split()

# Evolution rules for our automata
def evolve(inputs):
    outputs = []
    for i in range(len(inputs)):
        stone = inputs[i]
        if stone == ZERO:
            outputs.append(ONE)
            continue

        if len(stone) % 2 == 0:
            outputs.append(stone[:len(stone)//2])
            outputs.append(str(int(stone[len(stone)//2:])))
            continue

        outputs.append(str(int(stone) * 2024))
    return outputs

stones = get_inputs()
# stone_map is essentially our transition matrix
# seed w/ initial mappings from inputs
stone_map = {s: evolve([s]) for s in stones}

# probably could also have modeled this as a square matrix and multiplied it by itself 75 times
#for stone in itertools.chain(*next_iters.values()):
# map out every possible step that will be needed
print(b("Building node mapping..."))
should_continue = True
while should_continue:
    # Will stay false unless we find at least one value that doesn't exist yet
    should_continue = False
    for s in sum(stone_map.values(), []):
        if s not in stone_map:
            should_continue = True
            stone_map[s] = evolve([s])

# Each index of the child list represents an iteration
node_weights = {s: [0] for s in stone_map}

# Seed inputs at iteration -1 (index zero)
for s in stones:
    node_weights[s][0] += 1

print(id(0), g(sum([x[-1] for x in node_weights.values()])))
# range from 1 to 76 because index 0 contains iteration -1
for i in range(1, 76):
    for w in node_weights:
        # append row of zeros that will get filled out (like a poor man's defaultdict(int)
        node_weights[w].append(0)

    # add the weight of the parent to each child. I.e. if node 0 maps to node 1,
    # and node 0 is weight 2 (i.e. 2 paths have landed there), it will transfer
    # weight 2 to node 1
    for parent, children in stone_map.items():
        for stone in children:
            node_weights[stone][i] += node_weights[parent][i-1]

    # print each iteration
    print(id(i), g(sum([x[-1] for x in node_weights.values()])))
