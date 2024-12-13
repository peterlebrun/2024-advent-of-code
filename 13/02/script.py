import sys
import copy
from collections import defaultdict
import math
sys.setrecursionlimit(1073741824)

A = "A"
B = "B"
COST = [3, 1]
BUTTON_A = "Button A"
BUTTON_B = "Button B"
PRIZE = "Prize"
INT_SOLUTIONS = "INT_SOLUTIONS"
MODIFIER = 10000000000000
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

if sys.argv[1] not in ["input", "input_test"]:
    print("Invalid input file provided. Should be one of ", b("input "),
              "or ", b("input_test"))
    exit()

if len(sys.argv) > 2:
    print("Unrecognized arguments provided.")
    exit()

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = self._get_length()
        self.angle = self._get_angle()
        self.unit_vector = self._get_unit_vector()

    def __repr__(self):
        header = b(f"Vector ({self.x}, {self.y})") + "\n"
        length = f"Length: {g(self.length)}" + "\n"
        angle = f"Angle: {g(self.angle)}" + "\n"
        return f"{header}{length}{angle}"

    def _get_length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def _get_angle(self):
        return math.atan(self.y/self.x)

    def _get_unit_vector(self):
        if self.length == 1.0:
            return None
        return Vector(self.x/self.length, self.y/self.length)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        return Vector(other * self.x, other * self.y)

def get_inputs():
    inputs = []
    with open(sys.argv[1], "r") as f:
        for row in f.readlines():
            row = row.strip()
            if row.startswith(BUTTON_A):
                inputs.append({A: Vector(int(row[12:14]), int(row[-2:]))})
            elif row.startswith(BUTTON_B):
                inputs[-1][B] = Vector(int(row[12:14]), int(row[-2:]))
            elif row.startswith(PRIZE):
                x = row[9:].split(",")
                inputs[-1][PRIZE] = Vector(int(x[0]) + MODIFIER, int(x[1][3:]) + MODIFIER)
    return inputs

def get_gcd(a, b):
    init_a, init_b = a, b
    while b != 0:
        rem = a % b
        a = b
        b = rem
    print(f"GCD: {init_a}, {init_b}: {a}")
    return a

def get_lcm(a, b):
    return a * b // get_gcd(a, b)

def find_solutions_old(inputs):
    a, b, prize = inputs[A], inputs[B], inputs[PRIZE]

    if a.angle > b.angle:
        # Just assume that a has larger angle for now
        angle_diffs = b.angle - a.angle
        print(f"angle_diffs: {angle_diffs}")
        a_diff = prize.angle - a.angle
        print(f"a_diff: {a_diff}")
        b_diff = b.angle - prize.angle
        print(f"b_diff: {b_diff}")
        print(f"a_diff_%: {a_diff / angle_diffs}")
        print(f"b_diff_%: {b_diff / angle_diffs}")
        print(f"new_a_vec: {a.unit_vector * (a_diff / angle_diffs)}")
        print(f"new_b_vec: {b.unit_vector * (b_diff / angle_diffs)}")
        hypothetical_unit_vector = a.unit_vector * (a_diff / angle_diffs) + b.unit_vector * (b_diff / angle_diffs)
        print(f"hypothetical_unit_vector: {hypothetical_unit_vector}")
        input()

    if b.angle > a.angle:
        # Just assume that a has larger angle for now
        angle_diffs = b.angle - a.angle
        print(f"angle_diffs: {angle_diffs}")
        a_diff = prize.angle - a.angle
        print(f"a_diff: {a_diff}")
        b_diff = b.angle - prize.angle
        print(f"b_diff: {b_diff}")
        print(f"a_diff_%: {a_diff / angle_diffs}")
        print(f"b_diff_%: {b_diff / angle_diffs}")
        print(f"new_a_vec: {a.unit_vector * (a_diff / angle_diffs)}")
        print(f"new_b_vec: {b.unit_vector * (b_diff / angle_diffs)}")
        hypothetical_unit_vector = a.unit_vector * (a_diff / angle_diffs) + b.unit_vector * (b_diff / angle_diffs)
        print(f"hypothetical_unit_vector: {hypothetical_unit_vector}")
        input()

class Row():
    def __init__(self, *args):
        self.row = list(args)

    def __mul__(self, scalar):
        return Row(*[scalar * r for r in self.row])

    def __add__(self, other):
        return Row(*[r + o for r, o in zip(self.row, other.row)])

    def __sub__(self, other):
        return Row(*[r - o for r, o in zip(self.row, other.row)])

    def __repr__(self):
        return f"{self.row}"

    def __getitem__(self, index):
        if index <= len(self.row):
            return self.row[index]
        return None

def find_solutions(inputs):
    a, b, prize = inputs[A], inputs[B], inputs[PRIZE]
    x_gcd = get_gcd(a.x, b.x)
    y_gcd = get_gcd(a.y, b.y)

    if prize.x % x_gcd != 0 or prize.y % y_gcd != 0:
        print("Solution does not exist")

    r1 = Row(a.x, b.x, prize.x)
    r2 = Row(a.y, b.y, prize.y)
    a_lcm = get_lcm(a.x, a.y)
    b_lcm = get_lcm(b.x, b.y)

    button_a_presses = None
    button_b_presses = None

    a_lcm_combined = (r1 * (a_lcm // a.x)) - (r2 * (a_lcm // a.y))
    print(a_lcm_combined)
    if a_lcm_combined[2] % a_lcm_combined[1] == 0:
        button_b_presses = a_lcm_combined[2] // a_lcm_combined[1]

    b_lcm_combined = (r1 * (b_lcm // b.x)) - (r2 * (b_lcm // b.y))
    print(b_lcm_combined)
    if b_lcm_combined[2] % b_lcm_combined[0] == 0:
        button_a_presses = b_lcm_combined[2] // b_lcm_combined[0]

    return button_a_presses, button_b_presses

def print_solution(s_k, s_v, i):
    left_hand = f"{s_k[0]} * {i[A]} + {s_k[1]} * {i[B]}"
    right_hand = f"= {s_v['sum']}"
    cost = f"at cost {s_v['cost']}"
    print(r(left_hand), b(right_hand), g(cost))

cost = 0
for i in get_inputs():
    print_divider(DASH, HALF)
    for k, v in i.items():
        print_divider(DOT, QUARTER)
        print(id(k, 7), g(v))
    solutions = find_solutions(i)
    if solutions[0] and solutions[1]:
        cost += solutions[0] * 3 + solutions[1] * 1

print(f"Total Cost: {cost}")

# not using the code below but leaving it bc I like it
primes = []
for i in range(2, 101):
    if any([i % p == 0 for p in primes]):
        continue
    primes.append(i)

all_factors = {}
def factorize(num):
    if num in all_factors:
        return all_factors[num]

    factors = defaultdict(int)
    for p in primes[::-1]:
        if p > num:
            continue
        while num % p == 0:
            factors[p] += 1
            num /= p
    return factors

def get_lcm_old(a, b):
    # This is not wrong but it would be faster to do
    # a * b / gcd(a, b)
    if a > b and a % b == 0: return a
    if b > a and b % a == 0: return b

    a_factors = factorize(a)
    b_factors = factorize(b)

    product = 1
    for f in set(list(a_factors.keys()) + list(b_factors.keys())):
        product *= f**max(a_factors.get(f, 0), b_factors.get(f, 0))
    return product
