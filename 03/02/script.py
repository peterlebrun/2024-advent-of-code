import re
product_sum = 0

with open('input', 'r') as f:
    input_text = f.read()

is_enabled = True
for m in re.findall("do\(\)|mul\(\d+,\d+\)|don\'t\(\)", input_text):
    if m == "do()":
        is_enabled = True
        continue

    if m == "don't()":
        is_enabled = False
        continue

    if is_enabled and m.startswith("m"):
        nums = list(map(int, m[4:-1].split(',')))
        product_sum += nums[0] * nums[1]

print(product_sum)
