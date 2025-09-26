for j in range(i, M):
    myexactlog(7, 1)
    rem = (M - (i + j) % M) % M
    myexactlog(8, rem)
    if rem < j:
        myexactlog(9, 0)
        pass
    break