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