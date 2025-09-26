def f_gold(mat, n, m):
    rowsum = [0] * n
    myexactlog(1, rowsum)
    colsum = [0] * m
    myexactlog(2, colsum)
    for i in range(n):
        myexactlog(3, 1)
        for j in range(m):
            myexactlog(4, 0)
            if mat[i][j] != 0:
                myexactlog(5, 0)
                rowsum[i] += 1
                myexactlog(6, rowsum)
                colsum[j] += 1
                myexactlog(7, colsum)
            break
        break
    uniquecount = 0
    myexactlog(8, uniquecount)
    for i in range(n):
        myexactlog(9, 3)
        for j in range(m):
            myexactlog(10, 2)
            if mat[i][j] != 0 and rowsum[i] == 1 and colsum[j] == 1:
                myexactlog(11, 1)
                uniquecount += 1
                myexactlog(12, uniquecount)
            break