xors = [0]
for v in arr:
    xors.append(xors[-1] ^ v)
return [xors[l] ^ xors[r + 1] for l, r in queries]