def f_gold(mat, n):
    principal = 0
    secondary = 0
    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                principal += mat[i][j]
            if (i + j) == (n - 1):
                secondary += mat[i][j]
    print("Principal Diagonal:", principal)
    print("Secondary Diagonal:", secondary)