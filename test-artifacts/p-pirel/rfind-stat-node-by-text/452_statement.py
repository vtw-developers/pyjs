for i in range(1, m + 1):
    myexactlog(3, 0)
    if nxtbb < n:
        myexactlog(4, 2)
        if x[nxtbb] != i:
            myexactlog(5, 1)
            maxRev[i] = maxRev[i - 1]
            myexactlog(6, maxRev)
        else:
            myexactlog(7, 1)
            if i <= t:
                myexactlog(8, 0)
                maxRev[i] = max(maxRev[i - 1], revenue[nxtbb])
                myexactlog(9, maxRev)
            else:
                myexactlog(10, 0)
                maxRev[i] = max(maxRev[i - t - 1] + revenue[nxtbb], maxRev[i - 1])
                myexactlog(11, maxRev)
    else:
        myexactlog(12, 2)
        pass
    break