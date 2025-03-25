ans = t = 0
for a, b in sorted(zip(plantTime, growTime), key=lambda x: -x[1]):
    t += a
    ans = max(ans, t + b)
return ans