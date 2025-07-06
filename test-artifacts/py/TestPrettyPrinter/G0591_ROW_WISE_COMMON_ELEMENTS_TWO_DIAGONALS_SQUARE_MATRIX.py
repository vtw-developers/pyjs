def f_gold(mat, n):
    res = 0
    for i in range(n):
        if mat[i][i] == mat[i][n - i - 1]:
            res = res + 1
    return res