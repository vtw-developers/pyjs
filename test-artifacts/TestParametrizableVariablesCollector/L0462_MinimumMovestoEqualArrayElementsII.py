nums.sort()
k = nums[len(nums) >> 1]
return sum((abs(v - k) for v in nums))