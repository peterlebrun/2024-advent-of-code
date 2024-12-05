from collections import defaultdict
import sys
sys.setrecursionlimit(1073741824)

PIPE = "|"
COMMA = ","

rules = {}
rules_tree = {}
#priority = defaultdict(int)
unordered_updates = []
middle_sum = 0

def is_in_order(input_str, rules):
    vals = input_str.split(COMMA)

    for v in vals:
        #print(f"v: {v}")
        v_start = input_str.find(v)
        #print(f"v_start: {v_start}")

        try:
            for z in rules[v]:
                #print(f"z: {z}")
                z_start = input_str.find(z)
                #print(f"z_start: {z_start}")

                if z_start == -1:
                    continue

                if z_start < v_start:
                    #print("Not in order")
                    return False
        except KeyError:
            continue

    #print("In order")
    return True

priorities = []

used_nums = set()
with open('input', 'r') as f:
    for x in [r.strip() for r in f.readlines()]:
        if PIPE in x:
            pre, post = x.split(PIPE)

#case: pre in priorities (but not post)
#case: post in priorites (but not pre)
#case: neither in priorities
#case: both in priorities


            rules[pre].append(post)

            pre_vals[pre] += 1
            post_vals[post] += 1
            print("pre_vals")
            print(pre_vals)
            print("post_vals")
            print(post_vals)
            #input()

        elif COMMA in x:
            if not is_in_order(x, rules):
                unordered_updates.append(x)
                for y in x.split(COMMA):
                    used_nums.add(y)
                #un
                #int_vals = list(map(int, x.split(COMMA)))
                #print(f"int_vals: {int_vals}")
                #middle_index = int((len(int_vals) - 1) / 2)
                #print(f"middle_index: {middle_index}")
                #middle_sum += int_vals[middle_index]
                #print(f"middle_sum: {middle_sum}")

#print(middle_sum)
def get_child_rules(pre):
    for r in rules[pre]:
        return get_child_rules(r)

START = list(rules.keys())[0]
