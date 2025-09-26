def f_gold(mat, m, n, r):
    s = set()
    for j in range(n):
        s.add(mat[r][j])
    for i in range(m):
        if i == r:
            continue
        j = 0
        for j in range(n):
            if mat[i][j] not in s:
                j = j - 2
                break
        if j + 1 != n:
            continue