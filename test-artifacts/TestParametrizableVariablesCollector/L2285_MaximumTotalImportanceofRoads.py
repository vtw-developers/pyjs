deg = [0] * n
for a, b in roads:
    deg[a] += 1
    deg[b] += 1
deg.sort()
return sum((i * v for i, v in enumerate(deg, 1)))