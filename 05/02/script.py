from collections import defaultdict

PIPE = "|"
COMMA = ","

rules = defaultdict(set)
updates = []
sorted_middle_sum = 0
unsorted_middle_sum = 0

def is_in_order(input_str, rules):
    in_order = True
    applicable_rules = []
    vals = input_str.split(COMMA)

    for v in vals:
        v_start = input_str.find(v)

        try:
            for z in rules[v]:
                z_start = input_str.find(z)

                if z_start == -1:
                    continue

                if z_start < v_start:
                    in_order = False

                applicable_rules.append(f"{v}|{z}")
        except KeyError:
            continue

    return in_order, applicable_rules

def create_mapping():
    mapping = {}
    for x in rules:
        for y in rules:
            intersection = rules[x].intersection(rules[y])
            if len(intersection) == 23:
                x_diff = rules[x] - intersection
                if x_diff == set([y]):
                    mapping[x] = y
    return mapping

def create_sort_list(start):
    counter = 1
    priorities = { start: counter }

    val = mapping[start]
    while val != start:
        counter += 1
        priorities[val] = counter
        val = mapping[val]

    return priorities

def get_sorted_list(input_str, start):
    arr = input_str.split(COMMA)
    sort_list = create_sort_list(start)
    return ','.join(sorted(arr, key=lambda x: sort_list[x]))

def get_middle_val(input_str):
    arr = input_str.split(COMMA)
    middle = int((len(arr) - 1) / 2)
    return int(arr[middle])

with open('input', 'r') as f:
    for x in [r.strip() for r in f.readlines()]:
        if PIPE in x:
            pre, post = x.split(PIPE)
            rules[pre].add(post)

        elif COMMA in x:
            updates.append(x)

mapping = create_mapping()

for u in updates:
    in_order, applicable_rules = is_in_order(u, rules)

    if in_order:
        sorted_middle_sum += int(get_middle_val(u))
        continue

    else:
        pres = set()
        posts = set()

        for r in applicable_rules:
            pre, post = r.split("|")
            pres.add(pre)
            posts.add(post)

        start = None
        for x in pres:
            if x not in posts:
                start = x
                break

        sorted_list = get_sorted_list(u, start)
        unsorted_middle_sum += int(get_middle_val(sorted_list))

print(sorted_middle_sum)
print(unsorted_middle_sum)
