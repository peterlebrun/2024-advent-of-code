import sys
import copy
from collections import defaultdict
sys.setrecursionlimit(1073741824)

INPUT = "input_test" if len(sys.argv) > 1 and sys.argv[1] == "--test" else "input"

def print_divider():
    print("=" * 80)
    print("\n")

def plus(a, b):
    return a + b

def multiply(a, b):
    return a * b

ADD = "ADD"
MULTIPLY = "MULTIPLY"
CONCAT = "CONCAT"

evaluations = {}
with open(INPUT, 'r') as f:
    for row in f.readlines():
        result, inputs = row.split(":")
        result = int(result)

        evaluations[result] = list(map(int, inputs.split()))

#OPERATIONS = [plus, multiply]
OPERATIONS = [ADD, MULTIPLY, CONCAT]
#OPS_MAP = {
    #ADD: plus,
    #MULTIPLY: multiply,
#}

def create_graph(depth = 1):
    if depth == 1:
        return { k: None for k in OPERATIONS }

    return { k: create_graph(depth - 1) for k in OPERATIONS }

def get_children(graph, accumulator = []):
    children = []
    for k, v in graph.items():
        new_path = accumulator + [k]
        if v:
            children.extend(get_children(v, new_path))
        else:
            children.append(new_path)
    return children

def perform_operations(inputs, operations):
    inputs_copy = inputs.copy()
    operations_copy = operations.copy()

    res = inputs_copy.pop(0)
    while(len(inputs_copy)):
        operation = operations_copy.pop(0)
        if operation == ADD:
            res += inputs_copy.pop(0)
        if operation == MULTIPLY:
            res *= inputs_copy.pop(0)
        if operation == CONCAT:
            res = int(f"{res}{inputs_copy.pop(0)}")

    return res

def evaluate(inputs, result):
    for operations in get_children(create_graph(len(inputs) - 1)):
        if result == perform_operations(inputs, operations):
            return result
    return None

cum_sum = 0
init_results = []
updated_results = []
for result, inputs in evaluations.items():
    print(f"evaluating: {result}")
    r = evaluate(inputs, result)
    if r:
        cum_sum += r

print(cum_sum)

## stuff below is _really_ good but not at all necessary
#def get_all_permutations(n):
    #result = []
    #for i in range(2 ** n):
        #binary = bin(i)[2:].zfill(n)
        #result.append([bit == "1" for bit in binary])
    #return result

#def perform_concatenations(inputs):
    #concatenations = []
    #for p in get_all_permutations(len(inputs) - 1):
        ## use copy because popping is destructive action
        #inputs_copy = inputs.copy()
#
        ## move first element over so that inputs_copy is same length as p
        #tmp_inputs = [inputs_copy.pop(0)]
#
        #for i in range(len(inputs_copy)):
            #if p[i]:
                #tmp_inputs.append(int(f"{tmp_inputs.pop()}{inputs_copy.pop(0)}"))
            #else:
                #tmp_inputs.append(inputs_copy.pop(0))
#
        #concatenations.append(tmp_inputs)
#
    #return concatenations
