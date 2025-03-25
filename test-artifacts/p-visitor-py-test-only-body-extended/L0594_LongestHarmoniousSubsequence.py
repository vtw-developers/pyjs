counter = Counter(nums)
ans = 0
for num in nums:
    if num + 1 in counter:
        ans = max(ans, counter[num] + counter[num + 1])
return ans