d = {v: i for i, v in enumerate(nums)}
for a, b in operations:
    idx = d[a]
    d.pop(a)
    d[b] = idx
ans = [0] * len(nums)
for v, i in d.items():
    ans[i] = v
return ans