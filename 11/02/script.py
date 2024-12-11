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
    print_str("Exiting...")
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

def blink(inputs):
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
blink_map = {s: blink([s]) for s in stones}

#for stone in itertools.chain(*next_iters.values()):
should_continue = True
while should_continue:
    # Will stay false unless we find at least one value that doesn't exist yet
    should_continue = False
    for s in sum(blink_map.values(), []):
        if s not in blink_map:
            should_continue = True
            blink_map[s] = blink([s])

print(f"Length of blink map: {len(blink_map)}")

# just count the number of splits that occur
#for s in stones:
    #print_divider()
    #next_val = [s]
    #print(next_val)
    #num_splits = 0
    #for i in range(75):
        #tmp = []
        #for n in next_val:
            #tmp.extend(blink_map[n])
        #next_val = tmp
        #print(id(i), g(len(next_val)))
    #break

#for b, children in blink_tree.items():
node_weights
tree = {}
for s in stones:
    blink_tree =
