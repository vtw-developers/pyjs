prev = res = 0
for rung in rungs:
    res += (rung - prev - 1) // dist
    prev = rung
return res