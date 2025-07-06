def f_gold(mat, n, m):
    rowsum = [0] * n
    colsum = [0] * m
    for i in range(n):
        for j in range(m):
            if mat[i][j] != 0:
                rowsum[i] += 1
                colsum[j] += 1
    uniquecount = 0
    for i in range(n):
        for j in range(m):
            if mat[i][j] != 0 and rowsum[i] == 1 and colsum[j] == 1:
                uniquecount += 1
    return uniquecount