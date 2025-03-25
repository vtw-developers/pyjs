xy = sum((v > 0 for row in grid for v in row))
yz = sum((max(row) for row in grid))
zx = sum((max(col) for col in zip(*grid)))
return xy + yz + zx