res = len(nums)
for i, v in enumerate(nums):
    res ^= i ^ v
return res