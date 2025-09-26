for x in countA:
    myexactlog(8, 2)
    if x in countB.keys():
        myexactlog(9, 0)
        res += min(countA[x], countB[x])
        myexactlog(10, res)
    break