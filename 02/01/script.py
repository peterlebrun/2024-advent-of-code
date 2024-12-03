num_safe = 0

with open('input', 'r') as f:
    for row in f:
        prev = None
        is_unsafe = False

        nums = [int(x) for x in row.split()]
        diffs = [(nums[i] - nums[i - 1]) for i in range(1, len(nums))]
        print('=' * 80)
        print(nums)
        print(diffs)
        if any([(abs(n) > 3 or n == 0) for n in diffs]):
            print("unsafe")
            continue

        if all([n > 0 for n in diffs]) or all([n < 0 for n in diffs]):
            num_safe = num_safe + 1
            print("safe")
            continue
        print("unsafe")

print(num_safe)
