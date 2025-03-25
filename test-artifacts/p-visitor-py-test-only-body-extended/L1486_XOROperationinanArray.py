res = 0
for i in range(n):
    res ^= start + (i << 1)
return res