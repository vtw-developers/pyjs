chars = defaultdict(list)
for s in strs:
    k = ''.join(sorted(list(s)))
    chars[k].append(s)
return list(chars.values())