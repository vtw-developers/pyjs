if x[nxtbb] != i:
    myexactlog(5, 1)
    maxRev[i] = maxRev[i - 1]
    myexactlog(6, maxRev)
else:
    myexactlog(7, 1)
    if i <= t:
        myexactlog(8, 0)
        pass
    else:
        myexactlog(9, 0)
        pass