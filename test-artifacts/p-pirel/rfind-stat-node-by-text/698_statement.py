for j in range(m):
    myexactlog(10, 2)
    if mat[i][j] != 0 and rowsum[i] == 1 and colsum[j] == 1:
        myexactlog(11, 1)
        uniquecount += 1
        myexactlog(12, uniquecount)
    break