'\n    Do not return anything, modify nums in-place instead.\n    '
n = len(nums)
k %= n
if n < 2 or k == 0:
    return
nums[:] = nums[::-1]
nums[:k] = nums[:k][::-1]
nums[k:] = nums[k:][::-1]