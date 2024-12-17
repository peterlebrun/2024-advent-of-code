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

print_divider()
A, B, C, instructions = get_inputs()

def bitwise_xor(a, b):
    return (a & ~b) | (~a & b)

print(f"instructions: {instructions}")
print(f"A: {A}")
print(f"B: {B}")
print(f"C: {C}")
outputs = []
ptr = 0
while ptr < len(instructions) - 1:
    print_divider(DOT, QUARTER + 12)
    opcode, operand = instructions[ptr:ptr+2]
    combo = [0, 1, 2, 3, A, B, C]

    print_divider(DOT, 10)
    print(f"{ptr} {id(opcode, 2)} {g(operand)}")
    print_divider(DOT, QUARTER)
    # 0: A // 2 ** Combo Operand -> A
    if opcode == 0:
        tmp = A
        A = A // (2 ** combo[operand])
        print(f"A // 2 ** Combo Operand -> A")
        print(f"{r(tmp)} // 2 ** {r(combo[operand])} = {g(A)}")

    # 1: Bitwise XOR B|literal operand -> B
    if opcode == 1:
        print(f"B^literal_operand -> B")
        tmp = bitwise_xor(B, operand)
        print(f"({r(B)}^{r(operand)} = {g(tmp)}")
        B = tmp

    # 2: Combo operand % 8 -> B
    if opcode == 2:
        B = combo[operand] % 8
        print(f"Combo operand % 8 -> B")
        print(f"{r(combo[operand])} % 8 = {g(B)}")

    # 3: Nothing if A == 0, Otherwise jump instructions (do not increment pointer)
    if opcode == 3:
        print(f"Do nothing if A is zero. Otherwise set ptr to operand.")
        if A != 0:
            ptr = operand
            print(f"Setting ptr to {operand}.")
            if ptr < len(instructions) - 1:
                print(f"Program will now halt. Goodbye.")
            continue
        else:
            print(f"A is 0. Doing nothing.")

    # 4: Bitwise XOR B|C -> B (ignore operand)
    if opcode == 4:
        print(f"B^C -> B")
        tmp = bitwise_xor(B, C)
        print(f"({r(B)}^{r(C)} = {g(tmp)}")
        B = tmp

    # 5: Output Combo operand % 8
    if opcode == 5:
        outputs.append(str(combo[operand] % 8))
        print(f"Output combo[operand] % 8")
        print(f"{r(combo[operand])} % 8 = {outputs[-1]}")

    # 6: A // 2 ** Combo Operand -> B
    if opcode == 6:
        B = A // (2 ** combo[operand])
        print(f"A // 2 ** Combo Operand -> B")
        print(f"{r(A)} // 2 ** {r(combo[operand])} = {g(B)}")

    # 7: A // 2 ** Combo Operand -> C
    if opcode == 7:
        C = A // (2 ** combo[operand])
        print(f"A // 2 ** Combo Operand -> C")
        print(f"{r(A)} // 2 ** {r(combo[operand])} = {g(C)}")

    ptr += 2
    print(f"instructions: {instructions}")
    print(f"A: {A}")
    print(f"B: {B}")
    print(f"C: {C}")
    print(f"Outputs: {outputs}")
print_divider(DOT, HALF)
print(f"Outputs: {','.join(outputs)}")
