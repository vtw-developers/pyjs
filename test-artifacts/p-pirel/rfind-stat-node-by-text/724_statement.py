for i in range(0, M):
    myexactlog(6, 2)
    for j in range(i, M):
        myexactlog(7, 1)
        rem = (M - (i + j) % M) % M
        myexactlog(8, rem)
        break
    break