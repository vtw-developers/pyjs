mp = {}
for i, v in enumerate(nums):
    if v in mp and i - mp[v] <= k:
        return True
    mp[v] = i
return False