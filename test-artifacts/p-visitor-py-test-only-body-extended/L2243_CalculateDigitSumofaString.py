if len(s) <= k:
    return s
t = []
while s:
    t.append(str(sum((int(v) for v in s[:k]))))
    s = s[k:]
return f_gold(''.join(t), k)