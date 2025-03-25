mi, mx = (min(nums), max(nums))
return sum((mi < num < mx for num in nums))