def f_gold(mat, n):
    transpose = [[0] * n] * n
    for i in range(n):
        for j in range(n):
            transpose[i][j] = mat[j][i]