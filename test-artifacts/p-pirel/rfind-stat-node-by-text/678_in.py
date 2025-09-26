def f_gold(a, n, k):
    b = dict()
    myexactlog(1, b)
    for i in range(n):
        myexactlog(2, 0)
        x = a[i]
        myexactlog(3, x)
        d = min(1 + i, n - i)
        myexactlog(4, d)
        break