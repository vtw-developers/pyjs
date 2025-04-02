counter = [0] * 26
ans = 0
for c in s:
    i = ord(c) - ord('a')
    counter[i] += 1
    ans += counter[i]
return ans