def f_gold(a, n):
    count = dict()
    myexactlog(1, count)
    for i in range(n):
        myexactlog(2, 0)
        if count.get(a[i]):
            myexactlog(3, 0)
            count[a[i]] += 1
            myexactlog(4, count)
        else:
            myexactlog(5, 0)
            count[a[i]] = 1
            myexactlog(6, count)
        break
    next_missing = 1
    myexactlog(7, next_missing)
    for i in range(n):
        myexactlog(8, 1)
        if count[a[i]] != 1 or a[i] > n or a[i] < 1:
            myexactlog(9, 1)
            pass