def f_gold(mat, n):
    transpose = [[0] * n] * n
    myexactlog(1, transpose)
    for i in range(n):
        myexactlog(2, 1)
        for j in range(n):
            myexactlog(3, 0)
            transpose[i][j] = mat[j][i]
            myexactlog(4, transpose)
            break
        break
    flip = 0
    myexactlog(5, flip)
    for i in range(n):
        myexactlog(6, 3)
        for j in range(n):
            myexactlog(7, 2)
            if transpose[i][j] != mat[i][j]:
                myexactlog(8, 0)
                flip += 1
                myexactlog(9, flip)
            break
        break