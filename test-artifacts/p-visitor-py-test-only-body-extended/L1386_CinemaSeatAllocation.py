m = defaultdict(int)
for i, j in reservedSeats:
    m[i] = m[i] | 1 << 10 - j
masks = (480, 30, 120)
ans = n - len(m) << 1
for v in m.values():
    for mask in masks:
        if v & mask == 0:
            v |= mask
            ans += 1
return ans