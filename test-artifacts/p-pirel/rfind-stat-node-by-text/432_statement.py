for i in range(m):
    myexactlog(4, 2)
    if i == r:
        myexactlog(5, 0)
        continue
    j = 0
    myexactlog(6, j)
    for j in range(n):
        myexactlog(7, 1)
        if mat[i][j] not in s:
            myexactlog(8, 1)
            j = j - 2
            myexactlog(9, j)
            break
        break
    if j + 1 != n:
        myexactlog(10, 2)
        continue
    print(i)
    break