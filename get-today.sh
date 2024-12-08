#!/bin/bash
source ./get-cookie.sh
TODAY_LEADING_ZERO=$(date +'%d')
TODAY=$(date +'%-d')

echo $TODAY_LEADING_ZERO
echo $TODAY

mkdir -p $TODAY_LEADING_ZERO/01

curl \
--cookie $COOKIE \
https://adventofcode.com/2024/day/$TODAY/input \
-o $TODAY_LEADING_ZERO/01/input

cat <<EOF > $TODAY_LEADING_ZERO/01/script.py
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
    print(" ".join(args))

def print_divider(divider=EQUAL, length=FULL):
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

with open(INPUT, "r") as f:
    inputs = [[c for c in r.strip()] for r in f.readlines()]

num_rows = len(inputs)
num_cols = len(inputs[0])

for row in range(num_rows):
    for col in range(num_cols):
        pass
EOF
