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

def get_inputs():
    inputs = []
    with open(sys.argv[1], "r") as f:
        for row in f.readlines():
            row = row.strip()
            if row.startswith(BUTTON_A):
                inputs.append({A: (int(row[12:14]), int(row[-2:]))})
            elif row.startswith(BUTTON_B):
                inputs[-1][B]= (int(row[12:14]), int(row[-2:]))
            elif row.startswith(PRIZE):
                x = row[9:].split(",")
                inputs[-1][PRIZE] = (int(x[0]) + MODIFIER, int(x[1][3:]) + MODIFIER)
    return inputs

def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])

def mult(a, b):
    return a[0] * b[0] + a[1] * b[1]

def scale(vec, scalar):
    return (scalar * vec[0], scalar * vec[1])

def find_solutions(inputs):
    pass
    # find scalars c, d such that c * x_a = d * x_b, or c * y_a = d * y_b
    #find lcm

    #solutions = {}
    #for a in range(101):
        #a_scale = scale(inputs[A], a)
        #if a_scale[0] > inputs[PRIZE][0] or a_scale[1] > inputs[PRIZE][1]:
            #break
#
        #for b in range(101):
            #b_scale = scale(inputs[B], b)
            #if a_scale[0] > inputs[PRIZE][0] or a_scale[1] > inputs[PRIZE][1]:
                #break
#
            #vec_sum = plus(a_scale, b_scale)
            #if vec_sum == inputs[PRIZE]:
                #solutions[(a, b)] = {"sum": vec_sum, "cost": mult((a, b), COST)}
                #continue
            #if vec_sum[0] > inputs[PRIZE][0] or vec_sum[1] > inputs[PRIZE][1]:
                #break
    #return solutions

def print_solution(s_k, s_v, i):
    left_hand = f"{s_k[0]} * {i[A]} + {s_k[1]} * {i[B]}"
    right_hand = f"= {s_v['sum']}"
    cost = f"at cost {s_v['cost']}"
    print(r(left_hand), b(right_hand), g(cost))

cost = 0
for i in get_inputs():
    print_divider(DASH, QUARTER)
    for k, v in i.items():
        print(id(k, 7), g(v))
    #solutions = find_solutions(i)
    #min_cost = 0
    #for k, v in solutions.items():
        #print_solution(k, v, i)
        #if not min_cost or v['cost'] < min_cost:
            #min_cost = v['cost']
    #cost += min_cost
print(f"Total Cost: {cost}")

primes = []
for i in range(2, 101):
    if any([i % p == 0 for p in primes]):
        continue
    primes.append(i)

def factorize(num):
    factors = defaultdict(int)
    for p in primes[::-1]:
        if p > num:
            continue
        while num % p == 0:
            factors[p] += 1
            num /= p
    return factors

all_factors = {}

def get_lcm(a, b):
    if a > b and a % b == 0:
        return a
    if b > a and b % a == 0:
        return b

    all_factors[a] = all_factors.get(a, get_factors(a))
    all_factors[b] = all_factors.get(a, get_factors(a))

get_lcm(5, 10)
get_lcm(23, 44)
get_lcm(30, 91)

factorize(5)
factorize(10)
factorize(91)
