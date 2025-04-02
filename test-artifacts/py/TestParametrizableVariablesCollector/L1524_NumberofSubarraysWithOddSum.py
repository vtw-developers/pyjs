MOD = int(1000000000.0) + 7
counter = [0] * 2
s = ans = 0
for v in arr:
    s += v
    counter[s % 2] += 1
    if s % 2 == 1:
        ans += 1 + counter[0]
    else:
        ans += counter[1]
return ans % MOD