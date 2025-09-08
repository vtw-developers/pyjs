def f_gold(a, n, k):
    if k >= n - 1:
        myexactlog(1, 0)
        myexactlog(2, n)
        return n
    best = 0
    myexactlog(3, best)
    times = 0
    myexactlog(4, times)
    for i in range(n):
        myexactlog(5, 0)
        if a[i] > best:
            myexactlog(6, 2)
            best = a[i]
            myexactlog(7, best)
            if i:
                myexactlog(8, 1)
                pass
        else:
            myexactlog(9, 0)
            pass
        break