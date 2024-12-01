list1 = []
list2 = []
diff = 0

with open('input', 'r') as f:
    for line in f:
        nums = [int(x) for x in line.split()]
        list1.append(nums[0])
        list2.append(nums[1])

list1.sort()
list2.sort()

for n in range(len(list1)):
    diff = diff + abs(list1[n] - list2[n])
print(diff)
