n = len(nums)
return sum((i != j and nums[i] + nums[j] == target for i in range(n) for j in range(n)))