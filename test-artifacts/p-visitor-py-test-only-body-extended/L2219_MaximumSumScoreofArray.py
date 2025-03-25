s = [0] + list(accumulate(nums))
return max((max(s[i + 1], s[-1] - s[i]) for i in range(len(nums))))