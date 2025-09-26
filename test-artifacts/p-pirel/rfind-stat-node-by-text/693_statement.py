if i <= t:
    myexactlog(8, 0)
    maxRev[i] = max(maxRev[i - 1], revenue[nxtbb])
    myexactlog(9, maxRev)
else:
    myexactlog(10, 0)
    pass