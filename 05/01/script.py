from collections import defaultdict

PIPE = "|"
COMMA = ","

rules = defaultdict(list)
middle_sum = 0

def is_in_order(input_str, rules):
    vals = input_str.split(COMMA)

    for v in vals:
        print(f"v: {v}")
        v_start = input_str.find(v)
        print(f"v_start: {v_start}")

        try:
            for z in rules[v]:
                print(f"z: {z}")
                z_start = input_str.find(z)
                print(f"z_start: {z_start}")

                if z_start == -1:
                    continue

                if z_start < v_start:
                    print("Not in order")
                    return False
        except KeyError:
            continue

    print("In order")
    return True

with open('input', 'r') as f:
    for x in [r.strip() for r in f.readlines()]:
        if PIPE in x:
            pre, post = x.split(PIPE)
            rules[pre].append(post)

        elif COMMA in x:
            print(x)
            if is_in_order(x, rules):
                int_vals = list(map(int, x.split(COMMA)))
                print(f"int_vals: {int_vals}")
                middle_index = int((len(int_vals) - 1) / 2)
                print(f"middle_index: {middle_index}")
                middle_sum += int_vals[middle_index]
                print(f"middle_sum: {middle_sum}")

print(middle_sum)
