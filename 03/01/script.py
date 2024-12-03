import re
product_sum = 0

with open('input', 'r') as f:
    input_text = f.read()

for m in re.findall("mul\(\d+,\d+\)", input_text):
    nums = list(map(int, m[4:-1].split(',')))
    product_sum += nums[0] * nums[1]

print(product_sum)
