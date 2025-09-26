for i in range(n):
    myexactlog(5, 1)
    countB[b[i]] = countB.get(b[i], 0) + 1
    myexactlog(6, countB)
    break