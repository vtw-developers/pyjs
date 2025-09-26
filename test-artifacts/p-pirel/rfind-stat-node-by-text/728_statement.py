if i <= t:
    myexactlog(8, 0)
    maxRev[i] = max(maxRev[i - 1], revenue[nxtbb])
    myexactlog(9, maxRev)
else:
    myexactlog(10, 0)
    maxRev[i] = max(maxRev[i - t - 1] + revenue[nxtbb], maxRev[i - 1])
    myexactlog(11, maxRev)