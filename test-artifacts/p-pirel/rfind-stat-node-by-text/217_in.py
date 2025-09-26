def f_gold(mat, n, sum_0):
    for i in range(n):
        myexactlog(1, 0)
        mat[i].sort()
        myexactlog(2, mat)
        break
    for i in range(n - 1):
        myexactlog(3, 2)
        for j in range(i + 1, n):
            myexactlog(4, 1)
            left = 0
            myexactlog(5, left)
            right = n - 1
            myexactlog(6, right)
            break
        break