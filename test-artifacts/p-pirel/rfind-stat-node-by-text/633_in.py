def f_gold(mat, m, n):
    rowSum = [0] * m
    for i in range(0, m):
        sum_0 = 0
        for j in range(0, n):
            sum_0 += mat[i][j]
        rowSum[i] = sum_0