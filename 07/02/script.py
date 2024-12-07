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

evaluations = {}
with open(INPUT, 'r') as f:
    for row in f.readlines():
        result, inputs = row.split(":")
        result = int(result)

        evaluations[result] = list(map(int, inputs.split()))

#OPERATIONS = [plus, multiply]
OPERATIONS = [ADD, MULTIPLY]
#OPS_MAP = {
    #ADD: plus,
    #MULTIPLY: multiply,
#}

def create_graph(depth = 1):
    if depth == 1:
        return { k: None for k in OPERATIONS }

    return { k: create_graph(depth - 1) for k in OPERATIONS }

def get_children(graph, accumulator = []):
    #if not graph:
        #return accumulator
    children = []
    for k, v in graph.items():
        new_path = accumulator + [k]
        if v:
            children.extend(get_children(v, new_path))
        else:
            children.append(new_path)
    return children

cum_sum = 0
for result, inputs in evaluations.items():
    operations = get_children(create_graph(len(inputs) - 1))

    possible_results = set()
    for o in operations:
        inputs_copy = inputs.copy()
        o_copy = o.copy()

        res = inputs_copy.pop(0)
        while(len(inputs_copy)):
            operation = o_copy.pop(0)
            next_input = inputs_copy.pop(0)
            if operation == ADD:
                res += next_input
            if operation == MULTIPLY:
                res *= next_input
        possible_results.add(res)

    if result in possible_results:
        cum_sum += result

print(cum_sum)
