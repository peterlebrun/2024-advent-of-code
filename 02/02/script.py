num_safe = 0
unsafes = []

def is_safe(nums):
    diffs = [(nums[i] - nums[i - 1]) for i in range(1, len(nums))]
    if any([(abs(n) > 3 or n == 0) for n in diffs]):
        return False

    if all([n > 0 for n in diffs]) or all([n < 0 for n in diffs]):
        return True

    return False


with open('input', 'r') as f:
    for row in f:
        nums = [int(x) for x in row.split()]

        if is_safe(nums):
            num_safe += 1
        else:
            unsafes.append(nums)

for nums in unsafes:
    diffs = [(nums[i] - nums[i - 1]) for i in range(1, len(nums))]
    num_over_abs_3 = sum([1 if abs(x) > 3 else 0 for x in diffs])
    num_of_0 = sum([1 if x == 0 else 0 for x in diffs])
    num_gt_0 = sum([1 if (x > 0 and x <= 3) else 0 for x in diffs])
    num_lt_0 = sum([1 if (x < 0 and x >= -3) else 0 for x in diffs])

    # num_gt_0 + num_lt_0 = len nums

    num_violations = num_over_abs_3 + num_of_0

    if (num_gt_0 > 0 and num_gt_0 < num_lt_0):
        num_violations += num_gt_0
    if (num_lt_0 > 0 and num_lt_0 < num_gt_0):
        num_violations += num_lt_0


    print("="*80)
    print(nums)
    print(diffs)
    print(f"{num_over_abs_3} are over abs 3")
    print(f"{num_of_0} is 0")
    print(f"{num_gt_0} gt 0")
    print(f"{num_lt_0} lt 0")
    if num_violations == 1:
        print("pretty sure it's safe")
    if num_violations > 2:
        print("pretty sure it's not safe")
    if num_violations == 2:
        print("need to check if violations are adjacent")
    is_ok = False
    for i in range(len(nums)):
        new_copy = nums.copy()
        del new_copy[i]
        if is_safe(new_copy):
            is_ok = True
            break

    if is_ok:
        print("safe")
        num_safe += 1
    else:
        print("not safe")

#print(num_safe)
