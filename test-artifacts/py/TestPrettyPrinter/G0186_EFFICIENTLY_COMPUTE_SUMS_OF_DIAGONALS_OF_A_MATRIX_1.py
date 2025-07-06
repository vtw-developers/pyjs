def f_gold(mat, n):
    principal = 0
    secondary = 0
    for i in range(0, n):
        principal += mat[i][i]
        secondary += mat[i][n - i - 1]
    print("Principal Diagonal:", principal)
    print("Secondary Diagonal:", secondary)