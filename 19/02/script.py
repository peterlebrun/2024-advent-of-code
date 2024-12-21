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

def print_grid(grid, coords=(None, None), neighbors=set(), missing_vals=[]):
    top = " " * 5
    middle = " " * 5
    bottom = " " * 5
    for i in range(len(grid[0])):
        if i < 10:
            top += " "
            middle += " "
            bottom += f"{i}"
            continue
        elif i < 100:
            i = str(i)
            top += f" "
            middle += f"{i[0]}"
            bottom += f"{i[1]}"
        else:
            i = str(i)
            top += f"{i[0]}"
            middle += f"{i[1]}"
            bottom += f"{i[2]}"
    print(top)
    print(middle)
    print(bottom)
    for row_index, row in enumerate(grid):
        output = ""
        for col_index, col in enumerate(row):
            if (row_index, col_index) == coords:
                output += f"{g(col)}"
            elif (row_index, col_index) in neighbors:
                output += b("0")
            elif col == WALL:
                output += "\033[37;2m#\033[0m"
            elif (row_index, col_index) in missing_vals:
                output += f"\033[91;1;4m{col}\033[0m"
            else:
                output += f"\033[32;1m{col}\033[0m"
        print(f"{lpad(row_index, 3)}: {output}")

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

def insert(string, node):
    for key in node:
        if string.startswith(key):
            insert(string, node[key])
            return

        if key.startswith(string):
            node[string] = {key: node[key]}
            del node[key]
            return
    node[string] = {}

def generate_reverse_trie(string, node):
    is_child = False
    for key in node:
        if key.startswith(string):
            is_child = True
            generate_reverse_trie(string, node[key])
    if not is_child:
        node[string] = {}

def print_node(node, depth=0):
    pad = "-" * depth + (">" if depth else "")
    for key in node:
        print(f"{pad}{key}")
        print_node(node[key], depth+1)

def is_possible(row, trie):
    if not(row): return True

    node = trie
    while len(node):
        outer_loop_should_break = True
        for key in node:
            if row.startswith(key):
                if is_possible(row[len(key):], trie):
                    return True
                node = node[key]
                outer_loop_should_break = False
                break

        if outer_loop_should_break:
            break

    return False

def get_possibility(row, trie, possibility=[], depth=0, original_row=""):
    #print_divider(DASH, 5)
    if not original_row:
        original_row = row
    #print_divider(DASH, HALF)
    #print(f"row: {row}")
    #print(f"original_row: {original_row}")
    #print(f"possibility: {possibility}")
    #print(f"depth: {depth}")
    node = trie
    while len(node):
        #print(f"node: {node}")
        for key in node:
            #print(f"key: {key}")
            if row == key:
                #print(f"row = key {row}")
                if not depth: # this makes sure we don't return the string itself as a possibility
                    return []
                return [*possibility, key]

            if row.startswith(key):
                #print(f"row starts with {key}")
                if not any([row.startswith(k) for k in node[key]]):
                    #print(f"no longer key available")
                    return get_possibility(row[len(key):], trie, [*possibility, key], depth+1, original_row)
                else:
                    #print(f"traversing node instead")
                    node = node[key]
                    break

print_divider()
trie = {}
atoms = []
molecules = {}
with open(sys.argv[1], "r") as f:
    for index, row in enumerate(f.readlines()):
        row = row.strip()
        if index == 0:
            atoms = row.split(', ')
            atoms.sort(key=len)
            for a in atoms:
                insert(a, trie)
            print_node(trie)
            print_divider()

        if index >= 2:
            print(f"Evaluating row {index}: {row}")
            if is_possible(row, trie):
                molecules[row] = []

#for parent, children in molecules.items():
    #print_divider(DOT, HALF)
    #print(id(parent))
    #children.sort(key=len, reverse=True)
    #for atom in children:
        #print(atom)

#atom_store = {}
#for a in atoms:
#    print_divider()
#    possibility = get_possibility(a, trie, atom_store, [])
#    print(f"{a}: { possibility if len(possibility) else None }")
#    atom_store[a] = possibility

for_later = []
counter = 1
for m in molecules:
    if m in [
        "wwurggwbgwrrrbururuwggguwruwwrwbgubgwbrwbb",
        "rrbwwuguwgrrgrubggwrrgwbwbrubgruwgrrbwbrbbrguuwrgbwrwurwrb",
        "wwgwurwuwbgguubbbgurwburgubgbwwubwrbugubwgwggwwgrwwu",
        "rgrgugbuugbwrwbwwbururuwwgubbgburuwrrwrrwbb",
        "wguuuwgwwgbggbgubwbuwrbrrurubrgrrburruwbrgrwubgbuuburbw",
        "urgguubbrgguugbrrwrrbrwwuwwuwgurwuwbbwwbwwbrrurbburbrb",
        "wbubwuurugruwruuwbbbgbgwrbuwugbugrrgrburbbubbbubbrug",
    ]:
        for_later.append(m)
        continue
    print_divider(DASH, HALF)
    print(f"{counter} of {len(molecules)}")
    print(f"{m}")
    print(f"{get_possibility(m, trie)}")
    counter += 1
    input()
