def f_gold(a, n, k):
    b = dict()
    myexactlog(1, b)
    for i in range(n):
        myexactlog(2, 0)
        x = a[i]
        myexactlog(3, x)
        d = min(1 + i, n - i)
        myexactlog(4, d)
        if x not in b.keys():
            myexactlog(5, 0)
            b[x] = d
            myexactlog(6, b)
        else:
            myexactlog(7, 0)
            b[x] = min(d, b[x])
            myexactlog(8, b)
        break
    ans = 10 ** 9
    myexactlog(9, ans)
    for i in range(n):
        myexactlog(10, 1)
        x = a[i]
        myexactlog(11, x)
        if x != (k - x) and (k - x) in b.keys():
            myexactlog(12, 1)
            pass
        break