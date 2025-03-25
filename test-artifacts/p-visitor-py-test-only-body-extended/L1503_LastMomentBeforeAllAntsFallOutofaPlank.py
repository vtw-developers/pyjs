ans = 0
for t in left:
    ans = max(ans, t)
for t in right:
    ans = max(ans, n - t)
return ans