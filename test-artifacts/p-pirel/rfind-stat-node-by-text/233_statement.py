for j in range(1, n + 1):
    myexactlog(11, 2)
    if T[i - 1] != S[j - 1]:
        myexactlog(12, 1)
        mat[i][j] = mat[i][j - 1]
        myexactlog(13, mat)
    else:
        myexactlog(14, 0)
        pass
    break