def f_gold(mat, n, sum_0):
    for i in range(n):
        myexactlog(1, 0)
        mat[i].sort()
        myexactlog(2, mat)
        break