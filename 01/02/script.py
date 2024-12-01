from collections import defaultdict
list1 = defaultdict(int)
list2 = defaultdict(int)
similarity_score = 0

with open('input', 'r') as f:
    for line in f:
        nums = [x for x in line.split()]
        list1[nums[0]] = list1[nums[0]] + 1
        list2[nums[1]] = list2[nums[1]] + 1

for num in list1.keys():
    if num in list2:
        print(int(num), list1[num], list2[num])
        similarity_score = similarity_score + (int(num) * list1[num] * list2[num])

print(similarity_score)
