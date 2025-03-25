counter = Counter(nums)
return sum((num for num, cnt in counter.items() if cnt == 1))