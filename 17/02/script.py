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
    text = str(text)
    spaces = length - len(text)
    return f"{text}{' ' * spaces if spaces > 0 else ''}"

def lpad(text, length = 5):
    text = str(text)
    spaces = length - len(text)
    return f"{' ' * spaces if spaces > 0 else ''}{text}"

def id(num, length = 12):
    return b(rpad(f"{num}:", length))

def print_divider(divider=EQUAL, length=FULL):
    print(divider*length)

def exit():
    print("Exiting...")
    sys.exit()

if len(sys.argv) < 2:
    print("Please specify input file.")
    exit()

if not sys.argv[1].startswith("input"):
    print("Invalid input file provided.")
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

def get_inputs():
    A = None
    B = None
    C = None
    instructions = []
    with open(sys.argv[1], "r") as f:
        for row in f.readlines():
            row = row.strip()
            if "A" in row:
                A = int(row[12:])
            elif "B" in row:
                B = int(row[12:])
            elif "C" in row:
                C = int(row[12:])
            elif len(row):
                instructions = list(map(int, row[9:].split(',')))
        return A, B, C, instructions

def xor(a, b): return (a&~b)|(~a&b)

def run(A, B, C, instructions):
    outputs = []
    ptr = 0
    while ptr < len(instructions) - 1:
        opcode, operand = instructions[ptr:ptr+2]
        combo = [0, 1, 2, 3, A, B, C]

        if opcode == 0:
            tmp = A
            A = A // (2 ** combo[operand])

        if opcode == 1:
            tmp = xor(B, operand)
            B = tmp

        if opcode == 2:
            B = combo[operand] % 8

        if opcode == 3:
            if A != 0:
                ptr = operand
                continue

        if opcode == 4:
            tmp = xor(B, C)
            B = tmp

        if opcode == 5:
            outputs.append(combo[operand] % 8)
            print(outputs)
            for i in range(len(outputs)):
                if outputs[i] != instructions[i]:
                    print(f"No match: {outputs}")
                    return False, outputs

        if opcode == 6:
            B = A // (2 ** combo[operand])

        if opcode == 7:
            C = A // (2 ** combo[operand])

        ptr += 2
    return outputs

instructions = [2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0][::-1]
def calc(A):
    B = A & 0b111
    return xor(xor(xor(B, 0b10), A // 0b10 ** xor(B, 0b10)), 0b11) & 0b111

A = 0b1
ptr = 0
reset = None
counter = 0b0
tmp_outputs = []
while ptr < len(instructions):
    if calc(A) == instructions[ptr]:
        if ptr == len(instructions) - 1:
            break
        ptr += 1
        reset = A
        counter = 0b0
        A = A << 3
    else:
        if reset is not None:
            if counter == 0b111:
                A = reset
                ptr -= 1
                reset = None
                counter = 0b0
            else:
                counter += 0b1
        A += 0b1
print(A)

print_divider()
_, _, _, instructions = get_inputs()
run(A, 0, 0, instructions)
