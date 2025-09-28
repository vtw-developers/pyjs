def f_gold(a, n):
    count = dict()
    myexactlog(1, count)
    for i in range(n):
        myexactlog(2, 0)
        if count.get(a[i]):
            myexactlog(3, 0)
            pass
        else:
            myexactlog(4, 0)
            pass
        break