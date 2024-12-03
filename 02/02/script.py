num_safe = 0
unsafes = []

def is_safe(nums):
    diffs = [(nums[i] - nums[i - 1]) for i in range(1, len(nums))]
    print('=' * 80)
    print(nums)
    print(diffs)
    if any([(abs(n) > 3 or n == 0) for n in diffs]):
        return False

    if all([n > 0 for n in diffs]) or all([n < 0 for n in diffs]):
        return True

    return False


with open('input', 'r') as f:
    for row in f:
        nums = [int(x) for x in row.split()]

        if is_safe([int(x) for x in row.split()]):
            num_safe = num_safe + 1
        else:
            unsafes.append(nums)

for nums in unsafes:
    for i in range(len(nums)):
        new_copy = nums.copy()
        del new_copy[i]
        if is_safe(new_copy):
            num_safe = num_safe + 1
            break

print(num_safe)
