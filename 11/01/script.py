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

def print_str(*args):
    print(" ".join(map(str, args)))

def print_divider(divider=EQUAL, length=FULL):
    print(divider*length, "\n")

def exit():
    print_str("Exiting...")
    sys.exit()

if len(sys.argv) < 2:
    print_str("Please specify input file.")
    exit()

if sys.argv[1] not in ["input", "input_test"]:
    print_str("Invalid input file provided. Should be one of ", b("input "),
              "or ", b("input_test"))
    exit()

if len(sys.argv) > 2:
    print_str("Unrecognized arguments provided.")
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
            outputs.extend([stone[:len(stone)//2], str(int(stone[len(stone)//2:]))])
            continue

        outputs.append(str(int(stone) * 2024))
    return outputs

inputs = get_inputs()
print(inputs)
for i in range(25):
    inputs = blink(inputs)
    print_str(b(rpad(f"{lead_zero(i+1)}:")), g(inputs))

print(len(inputs))
