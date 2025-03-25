index = {c: i for i, c in enumerate(keyboard)}
res = t = 0
for c in word:
    res += abs(index[c] - t)
    t = index[c]
return res