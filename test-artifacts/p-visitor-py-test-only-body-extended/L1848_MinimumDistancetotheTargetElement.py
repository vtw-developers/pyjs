res = float('inf')
for i, num in enumerate(nums):
    if num == target:
        res = min(res, abs(i - start))
return res