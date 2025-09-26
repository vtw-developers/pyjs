for i in range(1, m + 1):
    for j in range(1, n + 1):
        if a[i - 1] == b[j - 1]:
            lookup[i][j] = lookup[i - 1][j - 1] + lookup[i - 1][j]
        else:
            lookup[i][j] = lookup[i - 1][j]