def f_gold(mat, n):
    flip = 0
    for i in range(n):
        for j in range(i):
            if mat[i][j] != mat[j][i]:
                flip += 1
    return flip