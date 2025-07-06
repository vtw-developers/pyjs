def f_gold(n):
    C = [[0 for x in range(n + 1)] for y in range(n + 1)]
    for i in range(n + 1):
        for j in range(min(i, n) + 1):
            if j == 0 or j == i:
                C[i][j] = 1
            else:
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    maxvalue = 0
    for i in range(n + 1):
        maxvalue = max(maxvalue, C[n][i])
    return maxvalue