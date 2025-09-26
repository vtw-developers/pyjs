def f_gold(mat, m, n, r):
    s = set()
    myexactlog(1, s)
    for j in range(n):
        myexactlog(2, 0)
        s.add(mat[r][j])
        myexactlog(3, s)
        break
    for i in range(m):
        myexactlog(4, 2)
        if i == r:
            myexactlog(5, 0)
            continue
        j = 0
        myexactlog(6, j)
        for j in range(n):
            myexactlog(7, 1)
            pass
            break
        break