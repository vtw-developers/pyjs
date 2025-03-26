n = len(grid)
for i, row in enumerate(grid):
    for j, v in enumerate(row):
        if i == j or i == n - j - 1:
            if v == 0:
                return False
        elif v:
            return False
return True