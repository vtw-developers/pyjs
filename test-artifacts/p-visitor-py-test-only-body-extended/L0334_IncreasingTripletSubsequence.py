mi, mid = (float('inf'), float('inf'))
for num in nums:
    if num > mid:
        return True
    if num <= mi:
        mi = num
    else:
        mid = num
return False