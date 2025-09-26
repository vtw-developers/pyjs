for j in range(1, n + 1):
    if T[i - 1] != S[j - 1]:
        mat[i][j] = mat[i][j - 1]
    else:
        mat[i][j] = mat[i][j - 1] + mat[i - 1][j - 1]