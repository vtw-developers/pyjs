def f_gold(mat, r, c):
    result = 0
    myexactlog(1, result)
    for i in range(r):
        myexactlog(2, 1)
        j = 0
        myexactlog(3, j)
        for j in range(c - 1):
            myexactlog(4, 0)
            if mat[i][j + 1] <= mat[i][j]:
                myexactlog(5, 0)
                break
            break
        if j == c - 2:
            myexactlog(6, 1)
            result += 1
            myexactlog(7, result)
        break
    for i in range(0, r):
        myexactlog(8, 3)
        j = 0
        myexactlog(9, j)
        for j in range(c - 1, 0, -1):
            myexactlog(10, 2)
            if mat[i][j - 1] <= mat[i][j]:
                myexactlog(11, 2)
                break
            break
        if c > 1 and j == 1:
            myexactlog(12, 3)
            result += 1
            myexactlog(13, result)