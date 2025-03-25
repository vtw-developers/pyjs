res = []
for c in s:
    if c not in {'a', 'e', 'i', 'o', 'u'}:
        res.append(c)
return ''.join(res)