ans = 0
for x in range(total // cost1 + 1):
    v = total - x * cost1
    ans += v // cost2 + 1
return ans