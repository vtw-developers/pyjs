costs.sort()
ans = 0
for c in costs:
    if coins < c:
        break
    else:
        ans += 1
        coins -= c
return ans