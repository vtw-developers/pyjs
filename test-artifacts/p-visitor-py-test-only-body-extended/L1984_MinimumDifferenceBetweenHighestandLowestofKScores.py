nums.sort()
return min((nums[i + k - 1] - nums[i] for i in range(len(nums) - k + 1)))