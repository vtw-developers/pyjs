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