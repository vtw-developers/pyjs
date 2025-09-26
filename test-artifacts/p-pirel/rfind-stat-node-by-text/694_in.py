def f_gold(a, b, n, m):
    countA = dict()
    myexactlog(1, countA)
    countB = dict()
    myexactlog(2, countB)
    for i in range(n):
        myexactlog(3, 0)
        countA[a[i]] = countA.get(a[i], 0) + 1
        myexactlog(4, countA)
        break
    for i in range(n):
        myexactlog(5, 1)
        countB[b[i]] = countB.get(b[i], 0) + 1
        myexactlog(6, countB)
        break
    res = 0
    myexactlog(7, res)
    for x in countA:
        myexactlog(8, 2)
        if x in countB.keys():
            myexactlog(9, 0)
            res += min(countA[x], countB[x])
            myexactlog(10, res)
        break