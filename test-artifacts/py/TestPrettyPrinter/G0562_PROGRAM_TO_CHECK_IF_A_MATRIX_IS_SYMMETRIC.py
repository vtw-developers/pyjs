def f_gold(mat, N):
    for i in range(N):
        for j in range(N):
            if mat[i][j] != mat[j][i]:
                return False
    return True